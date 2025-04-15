# Node-Based Image Processor 🎨⚙️

A desktop application for modular, node-based image manipulation. This tool allows users to construct visual image-processing pipelines using connected nodes—similar in style to tools like Substance Designer.

---

## 🚀 Features

- Visual node editor with drag-and-drop interface
- Load and save images through input/output nodes
- Real-time image previews
- Modular architecture to support custom processing nodes
- Built using Python, OpenCV, and PyQt5

---

## 🧠 Node Types (in progress)

| Category         | Node                          | Status       |
|------------------|-------------------------------|--------------|
| Basic            | ✅ Image Input Node            | Implemented |
|                  | ✅ Output Node                 | Implemented |
| Processing       | ✅ Brightness/Contrast Node    | Implemented |
|                  | ✅ Color Channel Splitter      | Implemented |
|                  | ✅ Gaussian Blur Node          | Implemented |
|                  | 🔧 Threshold Node              | Coming soon |
|                  | ✅ Edge Detection Node         | Implemented |
|                  | 🔧 Blend Node                  | Coming soon |
|                  | 🔧 Noise Generation Node       | Coming soon |
|                  | 🔧 Convolution Filter Node     | Coming soon |

---

## 🛠️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/SaanidhyaM/node-based-image-processor.git
cd node-based-image-processor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```
### 3. Run the app

```bash
python main.py
```
