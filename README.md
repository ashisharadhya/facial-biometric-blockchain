# Facial Biometric-Based Key Generation for Secure Data Storage

A facial biometric authentication system that generates secure cryptographic keys from facial landmarks, enabling identity-based encryption without storing raw biometric data.

> Built as part of a final-year B.Tech team project.

## Overview

This project explores how facial biometrics can be used to generate secure, repeatable cryptographic keys for authentication — eliminating the need to store passwords or raw biometric templates. Facial landmarks are extracted, processed, and used to derive a unique key per user through hashing, which can then be used for identity verification.

## Features

- Facial landmark extraction using MediaPipe Face Mesh
- Dimensionality reduction of facial feature vectors via Principal Component Analysis (PCA)
- Secure key generation using SHA-256 hashing
- API server for handling authentication requests
- CLI-based demo for testing the pipeline end-to-end

## Tech Stack

- **Language:** Python
- **Computer Vision:** MediaPipe Face Mesh, OpenCV
- **Cryptography:** SHA-256 hashing
- **ML:** Principal Component Analysis (PCA) for feature dimensionality reduction

## Project Structure

facial_keygen_system.py      # Core biometric processing and key generation logic
api_server.py                # API server for authentication requests
demo.py                       # CLI demo script
setup.py                      # Project setup/installation
production_requirements.txt   # Python dependencies

## Setup & Usage

1. Clone the repository:
```bash
   git clone https://github.com/ashisharadhya/facial-biometric-blockchain.git
   cd facial-biometric-blockchain
```

2. Install dependencies:
```bash
   pip install -r production_requirements.txt
```

3. Run the demo:
```bash
   python demo.py
```

4. Or start the API server:
```bash
   python api_server.py
```

## Author

- **Ashish A Aradhya** — [GitHub](https://github.com/ashisharadhya) · [LinkedIn](https://www.linkedin.com/in/ashish-a-aradhya-64975225a)

## Status

Core pipeline implemented — facial landmark extraction, PCA-based feature reduction, and SHA-256 key generation are functional. Future work may include blockchain integration for decentralized key storage.
