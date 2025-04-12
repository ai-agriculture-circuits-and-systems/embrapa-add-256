import os
import json
from PIL import Image
import glob
import argparse

def convert_to_coco(images_dir, annotations_file, output_file):
    """
    Convert Embrapa ADD 256 format annotations to COCO format.
    
    Args:
        images_dir (str): Directory containing the image files
        annotations_file (str): Path to the JSON file containing annotations
        output_file (str): Path to save the COCO format JSON file
    """
    # Initialize COCO format
    coco_format = {
        "info": {
            "description": "Embrapa Apples by Drones Detection Dataset (Embrapa ADD 256)",
            "version": "1.0",
            "year": 2021,
            "contributor": "Embrapa Agricultural Informatics",
            "date_created": "2021/10",
            "url": "https://github.com/thsant/add256"
        },
        "licenses": [
            {
                "id": 1,
                "name": "CC BY-NC 4.0",
                "url": "https://creativecommons.org/licenses/by-nc/4.0/"
            }
        ],
        "images": [],
        "annotations": [],
        "categories": [
            {
                "id": 1,
                "name": "apple",
                "supercategory": "fruit"
            }
        ]
    }
    
    # Load annotations
    with open(annotations_file, 'r') as f:
        annotations = json.load(f)
    
    annotation_id = 1
        
    for img_filename, apple_markers in annotations.items():
        # Get image info
        img_path = os.path.join(images_dir, img_filename)
        if not os.path.exists(img_path):
            print(f"Warning: Image file not found: {img_path}")
            continue
            
        img = Image.open(img_path)
        width, height = img.size
        
        # Add image info to COCO format
        img_id = len(coco_format["images"]) + 1
        coco_format["images"].append({
            "id": img_id,
            "license": 1,
            "file_name": img_filename,
            "height": height,
            "width": width,
            "date_captured": "2018-12-13"
        })
        
        # Convert apple markers to COCO format
        for marker in apple_markers:
            cx, cy = marker["cx"], marker["cy"]
            r = marker["r"]
            
            # Convert circle to bounding box
            x = cx - r
            y = cy - r
            w = h = 2 * r
            
            # Add annotation to COCO format
            coco_format["annotations"].append({
                "id": annotation_id,
                "image_id": img_id,
                "category_id": 1,
                "bbox": [x, y, w, h],
                "area": w * h,
                "segmentation": [],
                "iscrowd": 0
            })
            annotation_id += 1
    
    # Save to JSON file
    with open(output_file, 'w') as f:
        json.dump(coco_format, f, indent=2)
    
    print(f"Conversion complete. Created {len(coco_format['images'])} image entries and {len(coco_format['annotations'])} annotation entries.")
    print(f"COCO format JSON saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Embrapa ADD 256 format annotations to COCO format')
    parser.add_argument('--images', type=str, default="data/images", help='Directory containing the image files')
    parser.add_argument('--annotations', type=str, required=True, help='Path to the JSON file containing annotations (training.json or test.json)')
    parser.add_argument('--output', type=str, required=True, help='Path to save the COCO format JSON file')
    
    args = parser.parse_args()
    
    convert_to_coco(args.images, args.annotations, args.output)