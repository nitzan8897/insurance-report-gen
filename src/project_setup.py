import os

def create_directory_structure():
    """Create the project directory structure and __init__.py files"""
    # Define the directory structure
    directories = [
        'src',
        'src/gui',
        'src/data',
        'src/document'
    ]
    
    print("Creating directory structure...")
    
    # Create directories and __init__.py files
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        init_file = os.path.join(directory, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w', encoding='utf-8') as f:
                pass
        print(f"Created {directory} and its __init__.py")

    print("\nDirectory structure created successfully!")


if __name__ == "__main__":
    create_directory_structure()