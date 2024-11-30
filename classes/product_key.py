import random
import string
import os
import json
from typing import Optional, List, Dict

class ProductKeyManager:
    def __init__(self):
        self.agents_dir = "agents"
        os.makedirs(self.agents_dir, exist_ok=True)
    
    def generate_random_string(self, length: int) -> str:
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_product_keys(self, agent_name: str) -> List[str]:
        keys = []
        agent_prefix = agent_name[:3].upper()
        for i in range(100):
            key = (
                self.generate_random_string(4) +  # 4 random letters and numbers
                agent_prefix +                    # first 3 letters of agent name
                'r' +                            # literal 'r'
                str(i).zfill(3) +                # key index padded to 3 digits
                self.generate_random_string(5)    # 5 random letters
            )
            keys.append(key)
        return keys
    
    def create_agent_keys_file(self, agent_name: str) -> str:
        filename = os.path.join(self.agents_dir, f"{agent_name}.json")
        keys = self.generate_product_keys(agent_name)
        
        key_data = {
            str(i): {
                "key": keys[i],
                "activated_by": None
            } for i in range(len(keys))
        }
        
        with open(filename, 'w') as f:
            json.dump(key_data, f, indent=4)
            
        return filename
    
    def validate_product_key(self, key: str) -> Optional[str]:
        """Validates a product key and returns the agent filename if valid, None otherwise"""
        if len(key) != 16:  # 4 + 3 + 1 + 3 + 5 = 16 chars
            return None
            
        # Extract components
        agent_part = key[4:7]
        index_part = key[8:11]
        
        # Find matching agent file
        for filename in os.listdir(self.agents_dir):
            if filename.lower().startswith(agent_part.lower()):
                return filename
        
        return None
    
    def activate_key(self, key: str, username: str) -> bool:
        """Activates a product key for a user. Returns True if successful."""
        agent_file = self.validate_product_key(key)
        if not agent_file:
            return False
            
        filepath = os.path.join(self.agents_dir, agent_file)
        with open(filepath, 'r') as f:
            key_data = json.load(f)
            
        # Find the key in the data
        for index, data in key_data.items():
            if data["key"] == key:
                if data["activated_by"] is not None:
                    return False  # Key already activated
                    
                data["activated_by"] = username
                
                # Save updated data
                with open(filepath, 'w') as f:
                    json.dump(key_data, f, indent=4)
                return True
                
        return False