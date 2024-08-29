import torch


def load_yolo_model(model_type='yolov5s'):
    """
    Load a YOLOv5 model.

    Args:
        model_type (str): The model type to load ('yolov5s', 'yolov5m', 'yolov5l', 'yolov5x').

    Returns:
        torch.nn.Module: Loaded YOLOv5 model.
    """
    return torch.hub.load('ultralytics/yolov5', model_type, pretrained=True)
