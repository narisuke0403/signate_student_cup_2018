import preprocess
import train
import predict

if __name__ == "__main__":
    print("preprocess Start")
    preprocess.get_train_data()
    preprocess.get_test_data()

    print("train Start")
    train.full_train()

    print("predict Start")
    predict.past_predict()