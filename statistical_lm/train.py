import os
import pickle

from arg_parse import get_train_args  # isort:skip
from model import NGramLanguageModel, LaplaceLanguageModel  # isort:skip
from utils import load_data  # isort:skip

BOS = "<BOS>"  # hardcoded
EOS = "<EOS>"  # hardcoded


if __name__ == "__main__":

    # argparse
    args = get_train_args()

    # check path_to_save existence
    if os.path.exists(args.path_to_save):
        raise FileExistsError("save path already exists")

    # load data
    data = load_data(path=args.path_to_data, verbose=args.verbose)

    # train
    if args.smoothing is None:
        language_model = NGramLanguageModel(
            data=data,
            n=args.n,
            verbose=args.verbose,
        )
    elif args.smoothing == "add-k":
        language_model = LaplaceLanguageModel(
            data=data,
            n=args.n,
            delta=args.delta,
            verbose=args.verbose,
        )
    else:
        raise NotImplementedError(
            f"{args.smoothing} smoothing method is not implemented, "
            "use 'add-k' for Laplace smoothing or None in order to not to use any smoothing method"
        )

    # save
    os.makedirs("models", exist_ok=True)  # hardcoded "models" directory
    with open(args.path_to_save, "wb") as fp:
        pickle.dump(language_model, fp)
