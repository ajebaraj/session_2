import os 
import requests
import cv2
import shutil
import requests
import tqdm
from datetime import datetime
from xml.dom.minidom import parseString
from lxml import etree as ET
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import traceback
from database_settings import HTTP_BASE_URL
from collections import defaultdict
import requests
import traceback
import tqdm
import xml.etree.ElementTree as ET
from xml.dom import minidom
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
from io import BytesIO

def generate_xml(project_path, xml_filename, img_filename, image_width, image_height, image_dict, bounding_boxes):
    """
    This function will first parse the values to the xml and then generate the xml in the end
    """
    root = ET.Element("annotation")
    # Sub-elements for the root
    folder = ET.SubElement(root,'folder')
    folder.text = "project"
    filename = ET.SubElement(root, "filename")
    filename.text = image_dict['image_name']
    path = ET.SubElement(root,'path')
    path.text = os.path.join(project_path, img_filename)

    # Size information
    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    width.text = str(image_width)
    height = ET.SubElement(size, "height")
    height.text = str(image_height)
    depth = ET.SubElement(size, "depth")
    depth.text = str(3)

    # Iterate over bounding boxes and add object information
    for i, box in enumerate(bounding_boxes):
        obj = ET.SubElement(root, "object")
        name = ET.SubElement(obj, "name")
        name.text = image_dict['annotation_detection'][i]['cls'].strip()
        
        pose = ET.SubElement(obj, "pose")
        pose.text = "Unspecified"
        
        truncated = ET.SubElement(obj, "truncated")
        truncated.text = "0"
        
        difficult = ET.SubElement(obj, "difficult")
        difficult.text = "0"
        
        bndbox = ET.SubElement(obj, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        xmin.text = str(box['x_min'])
        ymin = ET.SubElement(bndbox, "ymin")
        ymin.text = str(box['y_min'])
        xmax = ET.SubElement(bndbox, "xmax")
        xmax.text = str(box['x_max'])
        ymax = ET.SubElement(bndbox, "ymax")
        ymax.text = str(box['y_max'])

    # Create a prettified XML string
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    
    # Save the XML to a file
    with open(os.path.join(project_path, xml_filename), "w") as xml_file:
        xml_file.write(xml_str)

def generate_video_xml(project_path, xml_filename, img_filename, image_width, image_height, image_name, bounding_boxes):
    """
    This function will first parse the values to the xml and then generate the xml in the end
    """
    root = ET.Element("annotation")
    # Sub-elements for the root
    folder = ET.SubElement(root,'folder')
    folder.text = "project"
    filename = ET.SubElement(root, "filename")
    filename.text = image_name
    path = ET.SubElement(root,'path')
    path.text = os.path.join(project_path, img_filename)

    # Size information
    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    width.text = str(image_width)
    height = ET.SubElement(size, "height")
    height.text = str(image_height)
    depth = ET.SubElement(size, "depth")
    depth.text = str(3)

    # Iterate over bounding boxes and add object information
    for i, box in enumerate(bounding_boxes):
        obj = ET.SubElement(root, "object")
        name = ET.SubElement(obj, "name")
        name.text = box['cls'].strip()
        
        pose = ET.SubElement(obj, "pose")
        pose.text = "Unspecified"
        
        truncated = ET.SubElement(obj, "truncated")
        truncated.text = "0"
        
        difficult = ET.SubElement(obj, "difficult")
        difficult.text = "0"
        
        bndbox = ET.SubElement(obj, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        xmin.text = str(box['x_min'])
        ymin = ET.SubElement(bndbox, "ymin")
        ymin.text = str(box['y_min'])
        xmax = ET.SubElement(bndbox, "xmax")
        xmax.text = str(box['x_max'])
        ymax = ET.SubElement(bndbox, "ymax")
        ymax.text = str(box['y_max'])

    # Create a prettified XML string
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    
    # Save the XML to a file
    with open(os.path.join(project_path, xml_filename), "w") as xml_file:
        xml_file.write(xml_str)

def check_dir_exists(project):
    print(f"\nCreating project dir name: {project}\n")
    if not os.path.exists(project):
        os.makedirs(project, exist_ok=True)

def get_image_coord(image_dict, width, height):
    """
    This function converts normalized coordinates to image coordinates.
    For bounding boxes: converts from (x_min, y_min, width, height) to (x_min, y_min, x_max, y_max)
    For polygons: finds the min and max x,y coordinates to create a bounding box
    """
    combined_cords = []
    for cords in image_dict['annotation_detection']:
        region_type = cords.get('region_type') or cords.get('regionType') or cords.get('type')
        if region_type == 'polygon' and 'points' in cords:
            # Handle polygon annotations
            points = cords['points']
            
            # Find min and max x,y coordinates from polygon points
            x_coords = [int(float(point['x']) * width) for point in points]
            y_coords = [int(float(point['y']) * height) for point in points]
            
            x_min_image_coord = min(x_coords)
            y_min_image_coord = min(y_coords)
            x_max_image_cord = max(x_coords)
            y_max_image_cord = max(y_coords)
            
        elif region_type == 'bounding_box' or region_type == None or region_type=="box":
            # Handle standard bounding box annotations
            x_min_image_coord = int(float(cords['x']) * width)
            y_min_image_coord = int(float(cords['y']) * height)
            w_image_coord = int(float(cords['w']) * width)
            h_image_cord = int(float(cords['h']) * height)
            
            x_max_image_cord = x_min_image_coord + w_image_coord
            y_max_image_cord = y_min_image_coord + h_image_cord
        else:
            print(f"Unknown annotation type: {region_type}")
            continue
        
        # Create and append coordinates dictionary regardless of annotation type
        coordinates = {'x_min': x_min_image_coord, 'y_min': y_min_image_coord,
                        'x_max': x_max_image_cord, 'y_max': y_max_image_cord }
        combined_cords.append(coordinates)
    return combined_cords

def download_frame_from_video(video, timestamp_ms):
    """
    Download a specific frame from a video at the given timestamp.
    
    Args:
    url (str): The URL of the video file
    timestamp_ms (int): Timestamp in milliseconds
    
    Returns:
    numpy.ndarray: The extracted frame as an image, or None if extraction fails
    """
    try:    
        # Set the video position
        video.set(cv2.CAP_PROP_POS_MSEC, timestamp_ms)
        
        # Read the frame
        success, frame = video.read()
        
        # Release the video capture object
        video.release()        
        if success:
            return frame
        else:
            print(f"Failed to extract frame at timestamp {timestamp_ms} ms")
            return None
    
    except Exception as e:
        print(f"Error downloading or processing video: {e}")
        return None


def get_video_coord(annotations, width, height):
    """
    This function will first convert the normalized coordinates to image coordinates
    Given the format from x_min, y_min, width, height of the object,
    the function will convert it to x_min, y_min, x_max, y_max
    """
    combined_cords = []
    for ann in annotations:
        if ann['region_type'] == 'bounding_box':
            x_min_image_coord = int(float(ann['x']) * width)
            y_min_image_coord = int(float(ann['y']) * height)
            w_image_coord =     int(float(ann['w']) * width)
            h_image_cord =      int(float(ann['h']) * height)
            cls = ann['cls']
            x_max_image_cord = x_min_image_coord + w_image_coord
            y_max_image_cord = y_min_image_coord + h_image_cord

            coordinates = {'x_min': x_min_image_coord, 'y_min': y_min_image_coord,
                            'x_max': x_max_image_cord, 'y_max': y_max_image_cord, 'cls': cls}
            combined_cords.append(coordinates)
    return combined_cords

def download_image_and_generate_xml(consolidated_dataset, usecase_id):
    """
    This function will download the images from the image URL from GCP cloud storage
    Get the object coordinates from normalized coordinates in x_min, y_min, x_max, y_max format
    Generate the xml file for training. 
    Save the image and the associated xml file in the folder.
    """

    # part_id = str(list_part_id_collection[0]['_id'])
    project_dir = os.path.join(os.getcwd(), usecase_id, 'data')
    check_dir_exists(project_dir)
    temp_video_dir = os.path.join(os.getcwd(), 'temp_video')
    check_dir_exists(temp_video_dir)
    for image_dict in tqdm.tqdm(consolidated_dataset, desc='Downloading data and generating train data'):
        # print(image_dict,"image_dict")
        doc_url = image_dict['file_url']
        print("doc_url :::", doc_url)
        if doc_url.startswith('http'):
            url = doc_url
        else:
            url = f"{HTTP_BASE_URL}{image_dict['file_url']}"
        img_file_name = url.split('/')[-1]
        # print("img_file_name :::",img_file_name)
        xml_file_name = os.path.splitext(img_file_name)[0] + '.xml'
        
        # print("xml_file_name :::",xml_file_name)
        video_flag = image_dict.get('is_video', False)
        if video_flag == False:
            response = requests.get(url, stream=True)
            try:
                with open(project_dir + '/' + img_file_name, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)

                img = cv2.imread(project_dir + '/' + img_file_name)
                width = int(img.shape[1])
                height = int(img.shape[0])

                if len(image_dict['annotation_detection']) > 0:
                    bounding_boxes = get_image_coord(image_dict, width, height)
                    if bounding_boxes:
                        generate_xml(project_dir, xml_file_name, img_file_name, width, height,
                                    image_dict, bounding_boxes)
            except Exception as e:
                traceback_info = traceback.format_exc()
                print(f"traceback: {traceback_info}")
                print(f"file corrupted {img_file_name}")
        
        if video_flag:
            try:
                # Download the video file
                response = requests.get(url, stream=True)
                response.raise_for_status()
                video_file_name = url.split('/')[-1]
                # Save the video to a temporary file
                with open(temp_video_dir + '/'+ video_file_name, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Open the video file
                video = cv2.VideoCapture(temp_video_dir + '/'+ video_file_name)
                # new_annotations = defaultdict(list)
                # for annotations in image_dict['annotation_detection']:
                #     new_annotations[annotations['start']].append(annotations)
                # Process all timestamps
                # for timestemp , annotations in new_annotations.items():
                for timestemp , annotations in consolidate_annotations_and_frames(
                    image_dict['annotation_detection']
                ).items():
                    try:   
                        print(timestemp,"time")
                        print(annotations,"ann")                     
                        # Reset video to beginning for each frame extraction
                        video.set(cv2.CAP_PROP_POS_MSEC, int(timestemp))
                        
                        # Capture frame
                        ret, image = video.read()
                        if not ret:
                            print(f"Failed to extract frame at timestamp {timestemp}")
                            continue
                        
                        frame_name = f"{os.path.splitext(video_file_name)[0]}_{timestemp}.jpg"
                        frame_xml_file_name = os.path.splitext(frame_name)[0] + '.xml'
                        width = int(image.shape[1])
                        height = int(image.shape[0])
                        bounding_boxes = get_video_coord(annotations, width, height)
                        if bounding_boxes:                  
                            generate_video_xml(project_dir, frame_xml_file_name, frame_name, width, height,
                                        frame_name, bounding_boxes)
                                # Save the frame
                            cv2.imwrite(os.path.join(project_dir, frame_name), image)
                    
                    except Exception as frame_error:
                        print(f"Error processing frame: {frame_error}")
                
                # Close video capture
                video.release()            
            except Exception as e:
                traceback.print_exc()
                # print(f"Error downloading or processing video: {e}")
                continue

def generate_seg_xml(project_path, xml_filename, img_filename, image_width, image_height, image_dict, bounding_boxes):
    """
    This function will first parse the values to the xml and then generate the xml in the end
    """    
    root = ET.Element("annotation")
    # Sub-elements for the root
    folder = ET.SubElement(root, 'folder')
    folder.text = "project"
    filename = ET.SubElement(root, "filename")
    filename.text = image_dict['image_name']
    path = ET.SubElement(root, 'path')
    path.text = os.path.join(project_path, img_filename)

    # Size information
    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    width.text = str(image_width)
    height = ET.SubElement(size, "height")
    height.text = str(image_height)
    depth = ET.SubElement(size, "depth")
    depth.text = str(3)

    # Iterate over bounding boxes and add object information
    for i, box in enumerate(bounding_boxes):
        # Only process if we have valid points
        if len(box) > 0:
            obj = ET.SubElement(root, "object")
            name = ET.SubElement(obj, "name")
            name.text = image_dict['annotation_detection'][i]['cls'].strip()
            
            pose = ET.SubElement(obj, "pose")
            pose.text = "Unspecified"
            
            truncated = ET.SubElement(obj, "truncated")
            truncated.text = "0"
            
            difficult = ET.SubElement(obj, "difficult")
            difficult.text = "0"
            
            polygon = ET.SubElement(obj, "polygon")
            print(f"Box: {box}")
            for point in box:
                print(f"Point: {point}")
                pt = ET.SubElement(polygon, "pt")
                x = ET.SubElement(pt, "x")
                x.text = str(point[0])
                y = ET.SubElement(pt, "y")
                y.text = str(point[1])

    # Create a prettified XML string
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    
    # Save the XML to a file
    with open(os.path.join(project_path, xml_filename), "w") as xml_file:
        xml_file.write(xml_str)

def download_seg_image_and_generate_xml(consolidated_dataset, usecase_id):
    """
    This function will download the images from the image URL from GCP cloud storage
    Get the object coordinates from normalized coordinates in x_min, y_min, x_max, y_max format
    Generate the xml file for training. 
    Save the image and the associated xml file in the folder.
    """    
    project_dir = os.path.join(os.getcwd(), usecase_id, 'data')
    check_dir_exists(project_dir)
    for image_dict in tqdm.tqdm(consolidated_dataset, desc='Downloading data and generating train data'):
        try:
            doc_url = image_dict['file_url']
            if doc_url.startswith('http'):
                url = doc_url
            else:
                url = f"{HTTP_BASE_URL}{image_dict['file_url']}"
            
            img_file_name = url.split('/')[-1]
            print("img_file_name :::", img_file_name)
            xml_file_name = img_file_name.split('.')[0] + '.xml'
            
            # Download the image
            response = requests.get(url, stream=True)
            
            with open(os.path.join(project_dir, img_file_name), 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            # Read the downloaded image to get dimensions
            img = cv2.imread(os.path.join(project_dir, img_file_name))
            if img is None:
                print(f"Error: Could not read image {img_file_name}")
                continue
                
            width = int(img.shape[1])
            height = int(img.shape[0])

            # Process annotations if they exist
            if len(image_dict['annotation_detection']) > 0:
                bounding_boxes = get_seg_image_coord(image_dict, width, height)
                print(f"Bounding boxes: {bounding_boxes}")
                if bounding_boxes:
                    generate_seg_xml(project_dir, xml_file_name, img_file_name, width, height,
                                image_dict, bounding_boxes)
                    print(f"Generated XML for {img_file_name}")
        except Exception as e:
            traceback_info = traceback.format_exc()
            print(f"Error: {e}")
            print(f"traceback: {traceback_info}")
            print(f"file corrupted or error occurred {img_file_name}")

def get_seg_image_coord(image_dict, width, height):
    """
    This function will convert the normalized coordinates to image coordinates for segmentation
    points
    """
    bounding_boxes = []
    for annotation in image_dict['annotation_detection']:
        region_type = annotation.get('region_type') or annotation.get('regionType') or annotation.get('type')
        if region_type == "polygon":  # Make sure points exist in the annotation
            image_points = []
            for point in annotation['points']:
                if 'x' in point and 'y' in point:
                    x_image_coord = int(float(point['x']) * width)
                    y_image_coord = int(float(point['y']) * height)
                    image_points.append((x_image_coord, y_image_coord))
            if image_points:  # Only append if we have points
                bounding_boxes.append(image_points)
        elif region_type == "bounding_box":
            # convert bbox to polygon points
            x_min_image_coord = int(float(annotation['x']) * width)
            y_min_image_coord = int(float(annotation['y']) * height)
            w_image_coord = int(float(annotation['w']) * width)
            h_image_coord = int(float(annotation['h']) * height)
            x_max_image_coord = x_min_image_coord + w_image_coord
            y_max_image_coord = y_min_image_coord + h_image_coord
            coordinates = [
                (x_min_image_coord, y_min_image_coord),
                (x_max_image_coord, y_min_image_coord),
                (x_max_image_coord, y_max_image_coord),
                (x_min_image_coord, y_max_image_coord)
            ]
            bounding_boxes.append(coordinates)
        else:
            print(f"Unknown annotation type: {region_type}")
    return bounding_boxes


def consolidate_annotations_and_frames(annotations):
    frame_coords = defaultdict(list)
    for annotation in annotations:
        main_frame = annotation.get('start', 0)
        region_type = annotation["region_type"]
        class_name = annotation["cls"]
        if all(k in annotation for k in ('x', 'y', 'w', 'h')):
            bbox_coordinates = {
                "x": annotation['x'],
                "y": annotation['y'],
                "w": annotation['w'],
                "h": annotation['h'],
                "region_type":region_type,
                "cls":class_name
            }
            frame_coords[main_frame].append(bbox_coordinates)

        effects = annotation.get('effects', {})
        for effect in effects:
            effect_frame = effect['effect_start']
            bbox_coordinates = {
                "x": effect["new_rectangles"]['x'],
                "y": effect["new_rectangles"]['y'],
                "w": effect["new_rectangles"]['w'],
                "h": effect["new_rectangles"]['h'],
                "region_type":region_type,
                "cls":class_name
            }
            frame_coords[effect_frame].append(bbox_coordinates)
    # result = [{frame: coords} for frame, coords in frame_coords.items()]
    # print(frame_coords)
    return frame_coords

#######################Classification#################################

def download_images_for_classification(consolidated_dataset, usecase_id, max_workers=8):
    project_dir = os.path.join(os.getcwd(), usecase_id)
    project_data_dir = os.path.join(project_dir, 'data')
    check_dir_exists(project_data_dir)

    labels_dict = {}

    def download_single_image(image_dict):
        url = image_dict.get('file_url')
        image_name = image_dict.get('image_name', url.split('/')[-1])
        is_labelled = image_dict.get('labelled', False)
        label = image_dict.get('classification_annotation', {}).get('class_label')

        # Skip if not labelled or label is missing
        if not is_labelled or not label:
            return f"[SKIP] Image {image_name} is not labelled or missing label.", None

        labels_dict[image_name] = label
        class_dir = os.path.join(project_data_dir, label)
        check_dir_exists(class_dir)
        image_path = os.path.join(class_dir, image_name)

        if os.path.exists(image_path):
            return f"[INFO] Image already exists: {image_name}. Skipping download.", image_name

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Validate image
            image = Image.open(BytesIO(response.content))
            image.verify()

            # Save valid image
            with open(image_path, 'wb') as f:
                f.write(response.content)

            return f"[SUCCESS] Downloaded {image_name}", image_name

        except Exception as e:
            return f"[ERROR] Failed to download or validate {image_name}: {e}", None

    # Parallel downloads
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_single_image, img) for img in consolidated_dataset]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading images"):
            msg, _ = future.result()
            print(msg)

    # Save labels.json
    labels_path = os.path.join(project_dir, 'labels.json')
    with open(labels_path, 'w') as f:
        json.dump(labels_dict, f, indent=2)

    # Print detected classes
    try:
        class_names = sorted([
            d for d in os.listdir(project_data_dir)
            if os.path.isdir(os.path.join(project_data_dir, d))
        ])
        print(f"\nDetected Classes ({len(class_names)}): {', '.join(class_names)}")
    except Exception as e:
        print(f"Failed to list class folders: {e}")

    print("\nImage download and validation completed.")


if __name__ == '__main__':
    pass