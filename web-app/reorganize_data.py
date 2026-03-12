import os
import shutil

base_data = r'd:\AI-Atlas\web-app\data'

# New structure definition
hierarchy = {
    "01-Foundations-of-AI": ["01-Intelligence-Definitions", "02-Agent-Frameworks", "03-History-of-AI"],
    "02-Classical-AI": ["01-Knowledge-Representation", "02-Search-Algorithms", "03-Planning-and-Decision-Making"],
    "03-Machine-Learning": ["01-Supervised-Learning", "02-Unsupervised-Learning", "03-Reinforcement-Learning", "04-Optimization"],
    "04-Deep-Learning": ["01-Neural-Network-Basics", "02-CNNs", "03-RNNs-and-LSTMs", "04-Transformers"],
    "05-Computer-Vision": ["01-Image-Perception", "02-Object-Recognition", "03-Spatial-Interaction"],
    "06-Natural-Language-Processing": ["01-Linguistics-and-Syntax", "02-Semantic-Analysis", "03-Speech-Processing"],
    "07-Generative-AI": ["01-Large-Language-Models", "02-Diffusion-Models", "03-Multimodal-Architectures"],
    "08-Autonomous-Systems": ["01-Robotics-Control", "02-SLAM", "03-Edge-AI"],
    "09-Frontier-Paradigms": ["01-Meta-Learning", "02-Causal-Inference", "03-Federated-Learning"],
    "10-Society-and-Ethics": ["01-Explainable-AI", "02-AI-Alignment", "03-Safety-and-Governance"]
}

def migrate():
    # Create new folders if they don't exist
    for pillar, subdomains in hierarchy.items():
        pillar_path = os.path.join(base_data, pillar)
        if not os.path.exists(pillar_path):
            os.makedirs(pillar_path)
            print(f"Created pillar: {pillar}")
        
        for sub in subdomains:
            sub_path = os.path.join(pillar_path, sub)
            if not os.path.exists(sub_path):
                os.makedirs(sub_path)
                # Add a placeholder file
                placeholder = os.path.join(sub_path, "01-introduction.txt")
                with open(placeholder, 'w') as f:
                    f.write(f"# {sub.replace('-', ' ')}\n\nIntroductory content for {sub} research.")

    print("Hierarchy updated successfully.")

if __name__ == "__main__":
    migrate()
