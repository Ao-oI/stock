import os
import zipfile

def create_deploy_zip(source_dir, output_filename):
    # Files/folders to exclude
    exclude_dirs = {'.git', '.idea', '__pycache__', 'venv', 'env', 'stock_env', 'log', 'target', 'cache', 'instock/cache', 'instock/log'}
    exclude_files = {'.gitignore', 'deploy_package.py', output_filename}

    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file in exclude_files:
                    continue
                if file.endswith('.pyc') or file.endswith('.zip'):
                    continue
                    
                file_path = os.path.join(root, file)
                # Calculate relative path for zip archive
                rel_path = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, rel_path)
    
    print(f"Deployment package created: {output_filename}")

if __name__ == "__main__":
    create_deploy_zip('.', 'stock_deploy.zip')
