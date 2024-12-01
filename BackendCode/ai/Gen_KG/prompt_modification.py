import os
import sys
from enum import Enum
from pydantic import BaseModel
from pathlib import  Path


path=str(Path(__file__).resolve().parent.parent)
sys.path.append(path)

from config.settings import PROMPTS_DIR


class PromptType(Enum):
    Entity_Extraction="entity_extraction"


class PromptPartType(Enum):
    PREFIX = "prefix"
    SUFFIX = "suffix"
    Example = "example"


class PromptModifier:
    def __init__(self,prompt_type:PromptType):

        self.default_path=PROMPTS_DIR/prompt_type.value
        self.prefix=self.prompt_loader(PromptPartType.PREFIX)
        self.example = self.prompt_loader(PromptPartType.Example)
        self.suffix = self.prompt_loader(PromptPartType.SUFFIX)
        self.prompt=self.prefix+self.example+self.suffix

    def add_prefix(self, prefix):
        """Add a prefix to the prompt."""
        self.prompt = f"{prefix} {self.prompt}"

    def add_suffix(self, suffix):
        """Add a suffix to the prompt."""
        self.prompt = f"{self.prompt} {suffix}"

    def replace_text(self, old_text, new_text):
        """Replace old text with new text in the prompt."""
        self.prompt = self.prompt.replace(old_text, new_text)

    def get_prompt(self):
        """Return the modified prompt."""
        return self.prompt

    def prompt_loader(self,part_type:PromptPartType):
        path=str(self.default_path)
        if not path.endswith(('/', '\\')):
            path += '/'  # 或者使用 '\\'，根据需要选择

        path += f"{part_type.value}.txt"  # 在原路径后添加 prefix.txt

        with open(path,'r',encoding='utf-8') as file:
            result=file.read()
            return result


# Example usage:
class EntityRelationshipConstructor:
    tuple_delimiter="\"{tuple_delimiter}\""
    tuple_delimiter_without = "\"{tuple_delimiter}"
    record_delimiter="{record_delimiter}"
    completion_delimiter="{completion_delimiter}"
    entity="\"entity"
    relationship = "\"relationship"


    def __init__(self,text,entity_types:list):
        """
        :param text:参考文本的信息
        :param entity_types:  就是实体类型 [person, technology, mission, organization, location]
        """
        self.text=text
        self.entity_types=entity_types
        self.entity_list=list()
        self.relationship_list = list()

    def add_single_entity_output(self,data:str,type_index:int,description:str):
        result=f"({self.entity}{self.tuple_delimiter}{data}{self.tuple_delimiter}{self.entity_types[type_index]}{self.tuple_delimiter}{description}\"){self.record_delimiter}"
        self.entity_list.append(result)
        return result

    def add_single_entity_output_dict(self,data:str,type_index:int,descript_dict:dict):
        description_dict=dict()
        result=f"({self.entity}{self.tuple_delimiter}{data}{self.tuple_delimiter}{self.entity_types[type_index]}{self.tuple_delimiter}{descript_dict}\"){self.record_delimiter}"
        self.entity_list.append(result)
        return result

    def remove_single_entity_output(self,index:int):
        self.entity_list.pop(index)

    def add_single_relationship_output(self,entity1:str,entity2:str,description:str,strength:int,isend:bool):
        result=""
        if isend is False:
            result+= f"({self.relationship}{self.tuple_delimiter}{entity1}{self.tuple_delimiter}{entity2}{self.tuple_delimiter}{description}{self.tuple_delimiter_without}{str(strength)}){self.record_delimiter}"
        else:
            result+= f"({self.relationship}{self.tuple_delimiter}{entity1}{self.tuple_delimiter}{entity2}{self.tuple_delimiter}{description}{self.tuple_delimiter_without}{str(strength)}){self.completion_delimiter}"
        self.relationship_list.append(result)
        return result

    def remove_single_relationship_output(self,index:int):
        self.relationship_list.pop(index)

    def get_final_prompt(self):

        result=""

        for entity in self.entity_list:
            result+=f"{entity}\n"

        for relationship in self.relationship_list:
            result+=f"{relationship}\n"

        return result



"""
a=EntityRelationshipConstructor("test_text",["A","B"])
print(a.construct_single_entity_output("a_test",0,"this is A test"))
print(a.construct_single_relationship_output("entity1","entity2","description",3,True))
print(a.construct_single_relationship_output("entity1","entity2","description",3,False))
"""




def modify_prompt(path):
    with open(path,'r',encoding='utf-8') as file:
        return file.read()


"""
--现代名:[白水晶]
-功效
--[石水]
|--功效:腹坚胀满
|--出处:《本草纲目》
|--原文:"石水，腹堅脹滿，煮酒服。
[肺痿]
|--功效:唾脓
|--出处:《本草纲目》
|--原文:"肺痿唾膿。

就有些古籍是会有这种故事情节的就 如果能提取出来就是直接一个卖点
典故？
"""

class JsonConstructor:
    def __init__(self,descript_list):
        self.descript_list=descript_list
        self.descript_dict=dict()
    def add_descript(self,descript:str,index:int):
        self.descript_dict[self.descript_list[index]]=descript
    def get_total_descript(self):
        return  self.descript_dict

if __name__=="__main__":
    pass