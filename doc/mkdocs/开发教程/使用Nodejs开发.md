# 使用Nodejs开发

# 暂未完工

### 1. 安装依赖包

打开命令行工具，进入 SDK 根目录，执行以下命令安装 Python 依赖包和 Nodejs 依赖包：

```bash
pip install -r requirements.txt
npm install
```

### 2. 使用示例

在 SDK 根目录下创建 Python 文件，例如 `main.js`，并将以下代码复制到文件中：

```javascript
# 导入库(ES6语法)
import { fly } from "./fhflyNode"

# 重写
const fh = fly()

# 调用 SDK 方法(异步)
await fh.move(0,100)

# 退出进程
process.exit()
```

### 3. 执行代码

执行前先确保串口驱动程序正常运行

```bash
node main.js
```


### 4. 开发接口文档

SDK 提供了丰富的开发接口，您可以参考以下文档了解更多使用方法和参数说明：

- **[SDK 接口文档](http://localhost:8000/接口文档/传感器控制/)**:  详细介绍了每个 SDK 方法的功能、参数和返回值。
