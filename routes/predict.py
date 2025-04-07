from flask import Blueprint, request, jsonify
import skimage.io
import torch
import torchvision.transforms as transforms
import torchxrayvision as xrv

predict_blueprint = Blueprint("predict", __name__)

@predict_blueprint.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        file = request.files['image']
        img = skimage.io.imread(file.stream)
        img = xrv.datasets.normalize(img, 255)

        if len(img.shape) > 2:
            img = img[:, :, 0]
        img = img[None, :, :]
        transform = transforms.Compose([xrv.datasets.XRayCenterCrop()])
        img = transform(img)

        model = xrv.models.get_model("densenet121-res224-all")

        with torch.no_grad():
            img = torch.from_numpy(img).unsqueeze(0)
            preds = model(img).cpu()
            output = [
                {"disease": key, "value": float(value)}
                for key, value in zip(xrv.datasets.default_pathologies, preds[0].detach().numpy())
            ]
        return jsonify(output)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
