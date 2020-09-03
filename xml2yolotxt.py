from xml.etree.ElementTree import ElementTree,Element
import os
import shutil
import tqdm

def file_name(file_dir):
    '''
    获取路径下所有文件
    此处用于获取train.txt、val.txt等
    '''
    file_list = []
    for files in os.listdir(file_dir):
        file_path = os.path.join(file_dir, files)
        if os.path.splitext(file_path)[1]=='.txt':
            file_list.append(file_path)
    return file_list

def read_xml(xml_path):
  '''''读取并解析xml文件
    in_path: xml路径
    return: ElementTree'''
  tree = ElementTree()
  tree.parse(xml_path)
  return tree


def convert(size, box):
    '''
    将标注的xml文件标注转换为darknet形的坐标
    '''
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

if __name__ == "__main__":
    pass
    # train txt
    txt_path = 'E:\\MachineLearning\\helmet\\VOC2028\\ImageSets\\Main'
    # 结尾带\\ linux改为/opt/images/的形式
    image_path = 'E:\\MachineLearning\\helmet\\VOC2028\\JPEGImages\\'
    xml_path = 'E:\\MachineLearning\\helmet\\VOC2028\\Annotations\\'

    output_path = 'E:\\MachineLearning\\helmet\\'
    output_image_path = output_path + 'images\\'
    output_label_path = output_path + 'labels\\'

    obj_name = ['hat','person','dog']

    txt_list = file_name(txt_path)
    for txt in txt_list:
        print('开始处理文件 ' + os.path.basename(txt))
        collection_name = os.path.basename(txt).split('.')[0]
        with open(txt, 'r') as f:
            i = 0
            label_dir = output_label_path + collection_name
            if not os.path.exists(label_dir):
                os.mkdir(label_dir)
            image_dir = output_image_path + collection_name
            if not os.path.exists(image_dir):
                os.mkdir(image_dir)
            for r in tqdm.tqdm(f.readlines()):
                f_name = r.strip()
                xml_name = f_name + '.xml'
                jpg_name = f_name + '.jpg'
                old_jpg = image_path + jpg_name
                new_jpg = image_dir + "\\" + jpg_name
                shutil.copy(old_jpg, new_jpg)

                xml_ = read_xml(xml_path + xml_name)
                width = float(xml_.find('size/width').text)
                height = float(xml_.find('size/height').text)
                size = (width, height)

                obj = xml_.findall('object')

                with open(label_dir + '\\' + f_name + '.txt', 'w+') as t:
                    for o in obj:
                        o_name = o.find('name').text
                        if not o_name in obj_name:
                            obj_name.append(o_name)
                            print(o_name + " 不属于人和帽子")
                        o_index = obj_name.index(o_name)

                        x1 = float(o.find('bndbox/xmin').text)
                        y1 = float(o.find('bndbox/ymin').text)
                        x2 = float(o.find('bndbox/xmax').text)
                        y2 = float(o.find('bndbox/ymax').text)
                        box = (x1,x2,y1,y2)
                        location = convert(size, box)
                        row = str(o_index) + " %.6f %.6f %.6f %.6f\n" % (location)
                        t.write(row)
                    t.flush()
    print(obj_name)

                        
                        

                



