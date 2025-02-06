import argparse
def device_parser():
    parser = argparse.ArgumentParser(description='Device configs')
    parser.add_argument('--use-cuda', type=bool, default=True, metavar='')
    parser.add_argument('--device-ids', type=str, default='[3]', metavar='')
    parser.add_argument('--num-devices', type=int, default=1, metavar='')
    parser.add_argument('--use-cudnn-benchmark', action='store_true', default=True)
    return parser

def train_parser():
    parser = argparse.ArgumentParser(description='Training configs')
    parser.add_argument('--batch-size', type=int, default=32, metavar='')
    parser.add_argument('--vali-batch-size', type=str, default=32, metavar='')
    parser.add_argument('--epochs', type=int, default=500, metavar='')
    parser.add_argument('--lr', type=float, default=0.0002, metavar='')   # REVIEW
    parser.add_argument('--momentum', type=float, default=0.5, metavar='')  # 动量
    parser.add_argument('--log-interval', type=int, default=10, metavar='')
    parser.add_argument('--outdir', type=str, default='/home/ljh/teststylegan/mystylegan/BFIRGB/out_dcgan_nbnetP_attr10_facenet_nbalign', metavar='')
    parser.add_argument('--imgdir', type=str, default='./dataset/nbalign_img', metavar='')
    parser.add_argument('--target_feature_type', type=str, default='facenet', metavar='')               # 仅extract_feature.py中有用
    parser.add_argument('--isResume', type=bool, default=False, metavar='')
    parser.add_argument('--lfwType', type=str, default='', metavar='')   # 0, 500, 14, loss, block
    return parser

def test_parser():
    parser = argparse.ArgumentParser(description='Testing configs')
    parser.add_argument('--batch-size', type=int, default=1, metavar='')
    parser.add_argument('--outdir', type=str, default='', metavar='')

def network_parser():
    # BFI
    parser = argparse.ArgumentParser(description='network configs')
    parser.add_argument('--nc', type=int, default=3)
    parser.add_argument('--ndf', type=int, default=128)
    parser.add_argument('--ngf', type=int, default=128) #128
    parser.add_argument('--nz', type=int, default=512) #512特征向量长
    parser.add_argument('--truncation', type=int, default=512)
    parser.add_argument('--c', type=float, default=50.)
    parser.add_argument(
        '--bfi_pretrain',
        type=str,
        default='/home/ljh/teststylegan/mystylegan/BFIRGB/out_dcgan_nbnetP_attr10_facenet_nbalign/inversion_epoch19.pth',
        metavar=''
        )
    return parser

def common_parser():
    parser = argparse.ArgumentParser(description='Common configs')
    parser.add_argument('--seed', type=int, default=666, metavar='')
    return parser


def dataset_parser():
    parser = argparse.ArgumentParser(description='Dataset configs')
    parser.add_argument('--data-path', type=str, default='/home/ljh/teststylegan/mystylegan/BFIRGB/dataset/facenet_lfw_rgb160_nbalign.npz', metavar='')
    parser.add_argument('--metric-data-path', type=str, default='/home/ljh/teststylegan/mystylegan/BFIRGB/dataset/facenet_lfw_rgb160_nbalign.npz', metavar='')
    parser.add_argument('--img-size', type=int, default=160, metavar='')
    parser.add_argument('--sr-size', type=int, default=512, metavar='')
    parser.add_argument('--num_workers', type=int, default=3, metavar='')
    parser.add_argument('--data-pin-memory', action='store_true', default=False)
    return parser

##############################################################################################
##############################################################################################
##############################################################################################

def get_main_parser(mode=None):
    parser = argparse.ArgumentParser(description='Main Application')

    # 添加模式无关的参数
    parser.add_argument('--some-common-arg', type=int, default=0, help='Some common argument')

    # 定义一个函数来添加子解析器的参数到主解析器
    def add_subparser_args(subparser, main_parser):
        for action in subparser._actions:
            if action.dest not in [a.dest for a in main_parser._actions]:
                main_parser._add_action(action)

    # 添加通用参数
    add_subparser_args(common_parser(), parser)
    add_subparser_args(device_parser(), parser)
    add_subparser_args(dataset_parser(), parser)
    add_subparser_args(network_parser(), parser)

    # 根据模式选择性地添加其他解析器的参数
    if mode == 'train':
        add_subparser_args(train_parser(), parser)
    elif mode == 'test':
        add_subparser_args(test_parser(), parser)

    return parser



if __name__ == '__main__':
    parser = get_main_parser(mode='train')
    print(parser)
    args = parser.parse_args()

    print(args)
