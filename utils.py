from lxml import etree
import numpy as np
import cv2

def parse_anno_file(cvat_xml):
    root = etree.parse(cvat_xml).getroot()
    anno = []
    for image_tag in root.iter('image'):
        image = {}
        for key, value in image_tag.items():
            image[key] = value
        image['shapes'] = []
        for poly_tag in image_tag.iter('polygon'):
            polygon = {'type': 'polygon'}
            for key, value in poly_tag.items():
                polygon[key] = value
            image['shapes'].append(polygon)

        image['shapes'].sort(key=lambda x: int(x.get('z_order', 0)))
        anno.append(image)

    return anno

def create_mask_file(annotation):
    size = (int(annotation['height']), int(annotation['width']))
    mask = np.zeros(size, dtype=np.uint8)
    for shape in annotation['shapes']:
        
        points = [tuple(map(float, p.split(','))) for p in shape['points'].split(';')]
        points = np.array([(int(p[0]), int(p[1])) for p in points])

        mask = cv2.fillPoly(mask, [points], color=255)
        
    return mask
        
# def create_mask_file(mask_path, width, height, bitness, color_map, background, shapes):
#     mask = np.full((height, width, bitness // 8), background, dtype=np.uint8)
#     for shape in shapes:
#         color = color_map.get(shape['label'], background)
#         points = [tuple(map(float, p.split(','))) for p in shape['points'].split(';')]
#         points = np.array([(int(p[0]), int(p[1])) for p in points])

#         mask = cv2.fillPoly(mask, [points], color=color)
    
#     return mask
#     cv2.imwrite(mask_path, mask)

# def create_empty_mask_file(mask_path, width, height, bitness, color_map, background, shapes):
#     mask = np.full((height, width, bitness // 8), background, dtype=np.uint8)
#     cv2.imwrite(mask_path, mask)