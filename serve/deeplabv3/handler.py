"""
Module for image segmentation default handler
"""
import torch
from torchvision import transforms as T
from ts.torch_handler.vision_handler import VisionHandler


class SegmentationHandler(VisionHandler):

    image_processing = T.Compose(
        [
            T.Resize(256),
            T.CenterCrop(224),
            T.ToTensor(),
            T.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
            ),
        ]
    )

    def postprocess(self, data):
        # Returning the class for every pixel makes the response size too big
        # (> 24mb). Instead, we'll only return the top class for each image
        data = data["out"]
        data = torch.nn.functional.softmax(data, dim=1)
        data = torch.max(data, dim=1)
        data = torch.stack(
            [data.indices.type(data.values.dtype), data.values], dim=3
        )

        return data.tolist()
