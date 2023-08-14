import os
import csv
import tkinter as tk
from tkinter import filedialog
import torch
from ultralytics.yolo.engine.predictor import BasePredictor
from ultralytics.yolo.engine.results import Results
from ultralytics.yolo.utils import DEFAULT_CFG, ROOT, ops


class DetectionPredictor(BasePredictor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_correct = 0
        self.total_incorrect = 0
        self.results_list = []  # To store the results

    def postprocess(self, preds, img, orig_imgs):
        """Postprocesses predictions and returns a list of Results objects."""
        preds = ops.non_max_suppression(preds,
                                        self.args.conf,
                                        self.args.iou,
                                        agnostic=self.args.agnostic_nms,
                                        max_det=self.args.max_det,
                                        classes=self.args.classes)

        results = []
        for i, pred in enumerate(preds):
            orig_img = orig_imgs[i] if isinstance(orig_imgs, list) else orig_imgs
            if not isinstance(orig_imgs, torch.Tensor):
                pred[:, :4] = ops.scale_boxes(img.shape[2:], pred[:, :4], orig_img.shape)
            path = self.batch[0]
            img_path = path[i] if isinstance(path, list) else path
            results.append(Results(orig_img=orig_img, path=img_path, names=self.model.names, boxes=pred))

            # Print predicted labels and file names
            labels = [self.model.names[int(label)] for label in pred[:, -1]]
            file_name = os.path.basename(img_path)
            print("Label yang Diprediksi:", labels)
            print("Nama File:", file_name)

            # Get the folder name from the file path
            folder_name = os.path.basename(os.path.dirname(img_path))

            # Check if the folder name matches the predicted label
            if folder_name.lower() == labels[0].lower():
                print("Prediksi Benar")
                self.total_correct += 1
            else:
                print("Prediksi Salah")
                self.total_incorrect += 1

            # Append the result to the results list
            self.results_list.append((file_name, labels[0], folder_name))

            print()

        return results

    def save_results_to_csv(self, file_path):
        """Save the results to a CSV file."""
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Nama File", "Label Prediksi", "Nama Folder"])
            writer.writerows(self.results_list)


def predict(cfg=DEFAULT_CFG, use_python=False):
    model = "models/best4.pt"

    root = tk.Tk()
    root.withdraw()

    # Set the default source folder path
    default_folder = "/Users/agstnmira/Documents/Skripsi/bisindo/images/val"
    source_folder = filedialog.askdirectory(title="Select Folder", initialdir=default_folder)
    if not source_folder:
        print("Folder tidak dipilih. Menggunakan folder bawaan:", default_folder)
        source_folder = default_folder

    args = dict(model=model, source=source_folder)

    if use_python:
        from ultralytics import YOLO
        YOLO(model)(**args)
    else:
        predictor = DetectionPredictor(overrides=args)
        predictor.predict_cli()

        # Save results to CSV file
        folder_name = os.path.basename(source_folder)
        save_path = os.path.join("/Users/agstnmira/Documents/Skripsi/deteksi-abjad-bisindo/prediksi", f"{folder_name}_results.csv")
        predictor.save_results_to_csv(save_path)

    print("Total Prediksi Benar:", predictor.total_correct)
    print("Total Prediksi Salah:", predictor.total_incorrect)


if __name__ == "__main__":
    predict()
