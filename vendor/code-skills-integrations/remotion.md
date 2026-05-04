# remotion

- **URL**: https://github.com/remotion-dev/remotion
- **License**: 见原仓库(Remotion License,商用条件下需购买)
- **类型**: 程序化视频生成框架 / "用 React 写视频"

## 这是什么

把 React 组件渲染成视频帧,通过 `useCurrentFrame()` 控制时间轴。可以在 Lambda 上并行渲染、可以做参数化(同一模板出不同语言/数据版本的 demo)、可以接入 CI 自动出片。

## 在 code-skills 中的对应

- **对应 skill**:`programmatic-video`
- **CLI 集成**:
  - `bin/code-skills demo init <project>` → `npx create-video`
  - `bin/code-skills demo render <id>` → `npx remotion render`
  - `bin/code-skills demo studio` → `npx remotion studio`

## 何时用

- 数据驱动的 demo(同模板不同数据)
- 多语言版本(同模板换字幕)
- CI 自动出片(每次发版重生成)
- 教程/课程的统一风格视频
- 个性化营销素材(每用户一份)

## 何时**不**用

- 一次性 demo(QuickTime 5 分钟搞定)
- 真实操作录屏(用 OBS 更直接)
- 终端类项目(用 asciinema 更轻)

## 怎么用

```bash
bin/code-skills demo init my-demo            # 初始化
cd my-demo
bin/code-skills demo studio                  # 浏览器预览
bin/code-skills demo render Main out.mp4     # 渲染
```

## 不集成的部分

- 把 remotion 打包进本仓库依赖(保持零依赖)
- Remotion Lambda 部署(那是 Remotion CLI 自己的功能)
- 商业 license 决策(根据上游条款)
