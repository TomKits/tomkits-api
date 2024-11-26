from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
import requests
import io

from models import History

predict_bp = Blueprint("predict", __name__)

# Mapping predicted class to disease details
disease_info = {
    "Bacterial_spot": {
        "nama_penyakit": "Bacterial Spot",
        "deskripsi": "Bacterial spot is a disease that affects tomato plants, causing lesions on leaves, stems, and fruit.",
        "solusi": "To control bacterial spot, use resistant varieties, remove infected plants, and apply copper-based fungicides.",
        "rekomendasi_product": "Copper sulfate fungicide, disease-resistant tomato seeds",
    },
    "Early_blight": {
        "nama_penyakit": "Early Blight",
        "deskripsi": "Early blight is caused by the fungus Alternaria solani and affects tomato plants, causing circular spots on leaves and stems.",
        "solusi": "Use fungicides like chlorothalonil or mancozeb, and practice crop rotation to prevent early blight.",
        "rekomendasi_product": "Chlorothalonil-based fungicides, disease-resistant tomato varieties",
    },
    "Healthy": {
        "nama_penyakit": "Healthy",
        "deskripsi": "The plant is healthy and shows no signs of disease.",
        "solusi": "No action required. Continue to care for the plant with proper watering, sunlight, and nutrients.",
        "rekomendasi_product": "General plant care products like fertilizers and organic growth enhancers",
    },
    "Late_blight": {
        "nama_penyakit": "Late Blight",
        "deskripsi": "Late blight is a devastating disease caused by the fungus Phytophthora infestans. It leads to rapid decay of leaves, stems, and fruit.",
        "solusi": "Apply fungicides like mefenoxam or metalaxyl and remove infected plant debris. Avoid overhead irrigation.",
        "rekomendasi_product": "Mefenoxam fungicides, metalaxyl fungicides",
    },
    "Leaf_mold": {
        "nama_penyakit": "Leaf Mold",
        "deskripsi": "Leaf mold is caused by the fungus Passalora fulva, and it affects the leaves, causing them to turn yellow and become moldy.",
        "solusi": "Improve air circulation around the plants, prune affected leaves, and apply fungicides like azoxystrobin.",
        "rekomendasi_product": "Azoxystrobin fungicides, tomato plant pruning shears",
    },
    "Mosaic_virus": {
        "nama_penyakit": "Mosaic Virus",
        "deskripsi": "Mosaic virus causes yellowing and mottling of tomato leaves, stunting growth and reducing yield.",
        "solusi": "Remove infected plants, control aphids (vectors), and consider using resistant tomato varieties.",
        "rekomendasi_product": "Aphid control products, virus-resistant tomato seeds",
    },
    "Septoria_leaf_spot": {
        "nama_penyakit": "Septoria Leaf Spot",
        "deskripsi": "Septoria leaf spot causes small, circular spots on the leaves, which eventually cause the leaves to die.",
        "solusi": "Use fungicides containing chlorothalonil or mancozeb, and remove infected leaves to reduce spread.",
        "rekomendasi_product": "Chlorothalonil fungicide, mancozeb fungicide",
    },
    "Spider_mites": {
        "nama_penyakit": "Spider Mites",
        "deskripsi": "Spider mites are small pests that cause yellowing and speckling of leaves, eventually leading to leaf drop.",
        "solusi": "Use miticides or insecticidal soap to control spider mites, and improve plant health by watering properly.",
        "rekomendasi_product": "Insecticidal soap, miticide",
    },
    "Target_spot": {
        "nama_penyakit": "Target Spot",
        "deskripsi": "Target spot causes dark, circular lesions on the leaves with a pale center, affecting tomato plants.",
        "solusi": "Apply fungicides like azoxystrobin or mancozeb and practice proper crop rotation to prevent further infections.",
        "rekomendasi_product": "Azoxystrobin fungicide, mancozeb fungicide",
    },
    "Yellow_leaf_curl_virus": {
        "nama_penyakit": "Yellow Leaf Curl Virus",
        "deskripsi": "This virus causes yellowing and curling of tomato leaves, often stunting plant growth.",
        "solusi": "Remove infected plants and control whitefly vectors. Use resistant tomato varieties when available.",
        "rekomendasi_product": "Whitefly control products, virus-resistant tomato seeds",
    },
}


@predict_bp.post("/disease")
@jwt_required()
def predict_disease():
    # Ensure the file is provided
    if "file" not in request.files:
        return jsonify({"Response Text": "Invalid file format"}), 400

    # Access the uploaded file
    image_file = request.files["file"]

    # Read the file content into a variable
    file_content = image_file.read()

    # Prepare the file for forwarding (prediction service)
    file_data = {
        "file": (
            image_file.filename,
            io.BytesIO(file_content),  # Create a fresh stream for forwarding
            image_file.mimetype,
        )
    }

    # Reset the original stream for further operations
    image_file.stream.seek(0)

    # URL of the prediction service
    url = "http://127.0.0.1:8080/predict"

    try:
        # Forward the file to the prediction service
        response = requests.post(url, files=file_data)

        # Parse the response text from the prediction service
        response_data = response.json()

        if "error" in response_data:
            return (
                jsonify({"Response Text": response_data["error"]}),
                response.status_code,
            )

        # If prediction response contains confidence and predicted class
        if "confidence" in response_data and "predicted_class" in response_data:
            # Convert to percentage
            confidence_percentage = round(response_data["confidence"] * 100, 2)
            predicted_class = response_data["predicted_class"]

            # Get disease details from the mapping
            disease = disease_info.get(predicted_class)

            if not disease:
                return jsonify({"Response Text": "Unknown disease"}), 500

            # Save the image to Google Cloud Storage
            image_url = History.save_image(image_file)

            return (
                jsonify(
                    {
                        "nama_penyakit": disease["nama_penyakit"],
                        "deskripsi": disease["deskripsi"],
                        "confidence": f"{confidence_percentage}%",
                        "solusi": disease["solusi"],
                        "rekomendasi_product": disease["rekomendasi_product"],
                        "image_url": image_url,
                    }
                ),
                response.status_code,
            )

        return (
            jsonify(
                {"response_text": "Unknown response format from prediction service"}
            ),
            500,
        )

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
