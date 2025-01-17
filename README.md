# 2D Anomaly Dataset Generator

🛠️ This project provides a tool for generating 2D anomaly datasets using a graphical user interface (GUI). It allows users to select an image, choose an anomaly, specify the number of anomalies, and apply optional noise to the generated dataset.

To set up the 2D-Anomaly-Dataset-Generator, create a new virtual environment with Python version 3.7.1 and install the required dependencies:

1. Create a virtual environment with Python 3.7.1:
    ```bash
    python3.7 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

1. Run `AG.py` to start the application:
    ```bash
    python AG.py
    ```
2. Click on the "🖼️ Select Image" button to choose a base image for generating anomalies.
3. Select an anomaly type from the provided options.
4. Enter the number of images with anomaly you wish to generate.
5. Choose the scale of the image from the dropdown menu.
6. Optionally, check the "Apply Noise" option to add noise to the generated images.
7. Click on the "⚙️ Generate" button to create your anomaly dataset.

![Software Interface](AG_image.png) 

## 📂 Anomalies and Masks

Anomalies and their corresponding masks are stored in the `an/` and `mask/` directories, respectively. The application automatically matches an anomaly with its corresponding mask during the dataset generation process. The generated anomalies are stored in the `results/` directory and their masks in the `masks/` folder.

## 📜 License

This project is open-source and available under the MIT License.
