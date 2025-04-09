import time

from llama_index.llms.mistralai import MistralAI
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import Document
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core import Settings
from typing import Dict, Any


class ToolExecutor:
    def __init__(self):
        self.output_storage:Dict[Any, Any]={}
        self.file_path:str=None

    async def execute_start_node(self, input_data=None, arg=None):
        pass

    async def execute_file(self, configs, arg=None):
        file_text = configs.fileText if hasattr(configs, 'fileText') else None
        filepath = configs.filepath if hasattr(configs, 'filepath') else None
        self.file_path = filepath
        return file_text

    async def execute_text_input(self, configs, arg=None):
        text = configs.Text if hasattr(configs, 'Text') else None
        return text

    async def execute_llm(self, configs, doc, arg=None):
        model = configs.modelName if hasattr(configs, 'modelName') else None
        temperature = configs.temperature if hasattr(configs, 'temperature') else None
        chat_input = configs.chat_input if hasattr(configs, 'chat_input') else None
        system_message = configs.system_message if hasattr(configs, 'system_message') else None
        api_key = configs.API_key if hasattr(configs, 'API_key') else None
        method = f"execute_{model.lower().replace('-','_').replace('.','_').replace(' ','_')}"
        print("----------------------------------------------")
        print(method)
        llm_method = getattr(self,method)
        if callable(llm_method):
            response = await llm_method(model=model, temperature=temperature, chat_input=doc, api_key=api_key, file=arg)
            return response

    async def execute_text_output(self, arg1=None, arg2=None, arg3=None, arg4=None):
        # print(arg1)
        return arg2
        # print(arg3)

    async def execute_tools(self, order, nodes, connections, execution_id, doc, *args, **kwargs) -> str:
        if order:
            for node in order:
                configs=nodes[node].config
                method=f"execute_{nodes[node].type.lower().replace(' ','_')}"
                tool_method=getattr(self, method, None)
                try:
                    if callable(tool_method):
                        input_to_be_given = None
                        for connection in connections:
                            if connection.to_node == node:
                                input_to_be_given = self.output_storage.get(nodes[connection.from_node].type.lower())
                                break

                        if input_to_be_given:
                            temp_output = await tool_method(configs, input_to_be_given, doc, *args, **kwargs)
                        else:
                            temp_output = await tool_method(configs, doc, *args, **kwargs)

                        if temp_output:
                            self.output_storage[nodes[node].type.lower()] = temp_output
                    else:
                        raise Exception(f"Method '{method}' not defined. Check node names.")
                except Exception as e:
                    raise e
        return self.output_storage['text output']
        # return 'abc'

    async def execute_mistral_small(self, model, temperature, chat_input, api_key, file:Document):
        llm = MistralAI(model=model, temperature=temperature, system_prompt=chat_input, api_key=api_key)
        embed_model = MistralAIEmbedding(model='mistral-embed', api_key=api_key)

        Settings.llm = llm
        Settings.embed_model = embed_model
        if isinstance(file, str):
            file = Document(text=file)
        # print(file.text)
        doc_index = VectorStoreIndex.from_documents([file])
        doc_engine = doc_index.as_query_engine(similarity_top_k=5)
        response = doc_engine.query(str(chat_input))
        return response
    
    async def execute_gemini_1_5_flash(self, model, temperature, chat_input, api_key, file: Document):
        # Initialize the Gemini LLM and embedding model
        llm = Gemini(model=f"models/{model}", temperature=temperature, system_prompt=chat_input, api_key=api_key)
        embed_model = GeminiEmbedding(model='gemini-embedding-exp', api_key=api_key)
    
        # Set the LLM and embedding model in the global settings
        Settings.llm = llm
        Settings.embed_model = embed_model
    
        # Ensure the file is a Document instance
        if isinstance(file, str):
            file = Document(text=file)
        # print(file.text)
    
        # Create a vector store index from the document
        doc_index = VectorStoreIndex.from_documents([file])
        doc_engine = doc_index.as_query_engine(similarity_top_k=5)
    
        # Query the document engine with the chat input
        response = doc_engine.query(str(chat_input))
        return response