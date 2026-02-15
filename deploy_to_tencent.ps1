$ServerIP = "82.156.114.132"
$User = "ubuntu"

Write-Host "=== 自动化部署脚本 ===" -ForegroundColor Cyan
Write-Host "目标服务器: $ServerIP"
Write-Host "用户名: $User"
Write-Host "提示: 执行过程中需要您手动输入服务器密码: xjchilli123!" -ForegroundColor Yellow

# 1. 重新打包
Write-Host "`n[1/3] 正在打包项目..." -ForegroundColor Green
conda run -n stock_env python create_deploy_zip.py

# 2. 上传文件
Write-Host "`n[2/3] 正在上传部署包..." -ForegroundColor Green
scp .\stock_deploy.zip ${User}@${ServerIP}:~/stock_deploy.zip

if ($LASTEXITCODE -ne 0) {
    Write-Host "上传失败。请检查网络或密码。" -ForegroundColor Red
    exit
}

# 3. 远程执行
Write-Host "`n[3/3] 正在远程执行部署..." -ForegroundColor Green
Write-Host "请再次输入密码以开始远程安装..." -ForegroundColor Yellow

$RemoteCommands = @'
    set -e
    
    echo "--> 清理 Docker 代理配置..."
    export http_proxy=""
    export https_proxy=""
    
    if [ -f /etc/systemd/system/docker.service.d/http-proxy.conf ]; then
        sudo mv /etc/systemd/system/docker.service.d/http-proxy.conf /etc/systemd/system/docker.service.d/http-proxy.conf.bak
        sudo systemctl daemon-reload
        sudo systemctl restart docker
        echo "--> Docker 代理已移除并重启服务"
    fi

    echo "--> 配置腾讯云镜像源..."
    sudo mkdir -p /etc/docker
    # 使用腾讯云内网镜像源（如果是腾讯云服务器，速度最快）
    echo '{"registry-mirrors": ["https://mirror.ccs.tencentyun.com"]}' | sudo tee /etc/docker/daemon.json
    sudo systemctl daemon-reload
    sudo systemctl restart docker

    echo "--> 安装解压工具..."
    sudo apt-get update
    sudo apt-get install -y unzip dos2unix

    echo "--> 解压部署包..."
    mkdir -p stock
    unzip -o ~/stock_deploy.zip -d stock
    cd stock
    
    # 确保换行符正确
    find . -type f -name "*.sh" -exec dos2unix {} \;

    echo "--> 配置 Nginx..."
    # 尝试适配两种常见的 Nginx 目录结构
    if [ -d /etc/nginx/conf.d ]; then
        sudo cp deployment/nginx.conf /etc/nginx/conf.d/in.ulife.vip.conf
    fi
    if [ -d /etc/nginx/sites-available ]; then
        sudo cp deployment/nginx.conf /etc/nginx/sites-available/in.ulife.vip
        sudo ln -sf /etc/nginx/sites-available/in.ulife.vip /etc/nginx/sites-enabled/
    fi
    sudo nginx -t && sudo systemctl reload nginx

    echo "--> 启动 Docker 服务 (编译 TA-Lib 可能需要 3-5 分钟，请耐心等待)..."
    # 判断 compose 命令版本
    if docker compose version > /dev/null 2>&1; then
        sudo docker compose up -d --build
    else
        sudo docker-compose up -d --build
    fi
    
    echo "--> 部署成功!"
'@

ssh -t ${User}@${ServerIP} $RemoteCommands

Write-Host "`n全部完成！请访问 http://in.ulife.vip" -ForegroundColor Cyan
