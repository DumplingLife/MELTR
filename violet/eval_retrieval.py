
from lib import *
from dataset import Dataset_Base
from model import VIOLET_Base
from agent import Agent_Base
import pandas as pd

class Dataset_Retrieval(Dataset_Base):
    def __init__(self, args, split):
        super().__init__(args)
        self.split = split
        
        dataset = args['dataset']
        self.imgs = pickle.load(open(f'./_data/{dataset}/img_{dataset}.pkl', 'rb'))
        self.vq = pickle.load(open(f'./_data/{dataset}/{dataset}_vq.pkl', 'rb'))

        if split == 'train':
            self.data = json.load(open(args['train_annotation'], 'r'))['sentences']
        else:
            self.data = json.load(open(args['test_annotation'], 'r'))['sentences']

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        vid = self.data[idx]['video_id']
        txt, mask = self.str2txt(self.data[idx]['caption'])
        
        img = []
        for b in self.imgs[vid]:
            img.append(self.str2img(b).unsqueeze(0))
        img = T.cat(img, dim=0)

        return img, txt, mask, vid

class Dataset_Product(T.utils.data.Dataset):
    def __init__(self, feat):
        super().__init__()
        
        self.vid2idx = {v: i for i, v in enumerate(feat)}
        self.lst = [[feat[p], feat[q]] for p in feat for q in feat]
        
    def __len__(self):
        return len(self.lst)
    
    def __getitem__(self, idx):
        p, q = self.lst[idx]
        
        return [p['feat_txt'], p['mask_txt'], self.vid2idx[p['video']], 
                q['feat_img'], q['mask_img'], self.vid2idx[q['video']]] # (p->text, q->video)

class VIOLET_Retrieval(VIOLET_Base):
    def __init__(self):
        super().__init__()
        
        self.fc = T.nn.Sequential(*[T.nn.Dropout(0.1), 
                                    T.nn.Linear(768, 768*2), T.nn.ReLU(inplace=True), 
                                    T.nn.Linear(768*2, 1)])
    
    def forward(self, typ, 
                img=None, txt=None, mask=None, 
                feat_img=None, mask_img=None, feat_txt=None, mask_txt=None):
        
        if typ=='feat':
            feat_img, mask_img, feat_txt, mask_txt = self.go_feat(img, txt, mask)
            return feat_img, mask_img, feat_txt, mask_txt
        
        elif typ=='cross':
            out, _ = self.go_cross(feat_img, mask_img, feat_txt, mask_txt)
            out = self.fc(out[:, feat_img.shape[1], :]).squeeze()
            return out

if __name__=='__main__':
    args = json.load(open(sys.argv[1], 'r'))
    args['size_batch'] = 100*T.cuda.device_count()
    print(args)
    
    model = T.nn.DataParallel(VIOLET_Retrieval().cuda())
    model.module.load_ckpt(args['path_ckpt'])
    model.eval()
    
    for split in ['val']:
        dl = T.utils.data.DataLoader(Dataset_Retrieval(args, split), 
                                     batch_size=args['size_batch'], shuffle=False, 
                                     num_workers=64, pin_memory=True)
        feat = {}
        for img, txt, mask, vid in tqdm(dl, ascii=True):
            with T.no_grad():
                feat_img, mask_img, feat_txt, mask_txt = model(typ='feat', img=img.cuda(), txt=txt.cuda(), mask=mask.cuda())
            for v, f_i, m_i, f_t, m_t in zip(vid, *[d.data.cpu().numpy() for d in [feat_img, mask_img, feat_txt, mask_txt]]):
                feat[v] = {'video': v, 'feat_img': f_i, 'mask_img': m_i, 'feat_txt': f_t, 'mask_txt': m_t}
        
        dl = T.utils.data.DataLoader(Dataset_Product(feat), 
                                     batch_size=args['size_batch'], shuffle=False, 
                                     num_workers=64, pin_memory=True)
        rank = {}
        for feat_txt, mask_txt, idx_txt, feat_img, mask_img, idx_vid in tqdm(dl, ascii=True):
            with T.no_grad():
                out = model(typ='cross', feat_img=feat_img, mask_img=mask_img, feat_txt=feat_txt, mask_txt=mask_txt)
                out = T.sigmoid(out).data.cpu().numpy()
            for i_t, i_v, o in zip(idx_txt, idx_vid, out):
                i_t, i_v, o = int(i_t), int(i_v), float(o)
                
                if not i_t in rank:
                    rank[i_t] = []
                rank[i_t].append([i_v, o])
        
        res = {'r@1': 0, 'r@5': 0, 'r@10': 0, 'median': []}
        for i_t in rank:
            tmp = sorted(rank[i_t], key=lambda d: -d[1])
            p = [d[0] for d in tmp].index(i_t)+1
            
            if p<=1:
                res['r@1'] += 1.0/len(rank)
            if p<=5:
                res['r@5'] += 1.0/len(rank)
            if p<=10:
                res['r@10'] += 1.0/len(rank)
            res['median'].append(p)
        res['median'] = int(np.median(res['median']))
        
        print(split, res)
        with open('result.txt', 'a') as f:
            text = f"r@1: {res['r@1']}, r@5: {res['r@5']}, r@10: {res['r@10']}, median: {res['median']}\n"
            f.write(text)