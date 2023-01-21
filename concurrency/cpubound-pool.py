import multiprocessing as mp
from argparse import ArgumentParser

from utils import timer


def much_cpu(n: int) -> int:
    return sum((i * i) ** 2 for i in range(n))


@timer
def do_lots_of_ops(params: list) -> None:
    with mp.Pool(20) as pool:
        print('Starting computation using process pool')
        pool.map(much_cpu, params)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-n', '--n-params', type=int, default=20, help='Number of params to compute')
    args = parser.parse_args()

    params = [5_000_000 + i for i in range(args.n_params)]
    do_lots_of_ops(params)
