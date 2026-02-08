#!/bin/bash

# 快速部署脚本

echo "🚀 开始部署快传..."

# 创建数据目录
mkdir -p data/uploads

# 构建并启动服务
docker-compose up -d --build

echo "✅ 部署完成！"
echo ""
echo "📝 访问地址："
echo "  前端: http://localhost"
echo "  后端: http://localhost:8000"
echo "  API文档: http://localhost:8000/docs"
echo ""
echo "📊 查看日志："
echo "  docker-compose logs -f"
