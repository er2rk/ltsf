import torch, train

train.args = train.parser.parse_args(['--layer', '2'])
model = train.Net(5, 1).eval()

def run(x):
    with torch.no_grad():
        return model.dense(model.mamba(model.proj(x)))  # skips the Tanhshrink so outputs aren't squashed to ~0

torch.manual_seed(0)
x = torch.randn(1, 200, 5)
x2 = x.clone()
x2[:, 150:] += torch.randn(1, 50, 5)  # change only the last 50 days

y, y2 = run(x), run(x2)
print('early days, max diff:', (y[:, :150] - y2[:, :150]).abs().max().item())
print('late days,  max diff:', (y[:, 150:] - y2[:, 150:]).abs().max().item())