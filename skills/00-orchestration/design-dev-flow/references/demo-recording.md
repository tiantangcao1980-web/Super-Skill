# Demo 视频录制模式

> 借鉴:[remotion-dev/remotion](https://github.com/remotion-dev/remotion) — 用 React 程序化生成视频。
> 核心思想:**用代码写视频,而不是录屏 + 剪辑**。可重放、可参数化、可 CI 化。

本文件回答:
- 什么时候录视频?(以及什么时候不录)
- 30 秒 demo 的标准结构
- 录屏 vs 程序化生成怎么选

---

## 一、什么时候做 Demo

### 必做
- 给老板/投资人演示
- README 顶部(开源项目)
- 提交到 ProductHunt / 黑客松
- 内部分享会(替代 PPT 的最后一页)

### 可选
- PR 描述(改了交互)
- 给客服/销售的功能介绍
- A/B 实验对比

### 不做
- 内部工具
- 仅 CLI 项目
- 还在 alpha 阶段(过几周就变了,白录)

---

## 二、30 秒 Demo 的标准结构

```
[0-3s]   钩子 — 一句话/一画面让观众停下
[3-10s]  问题 — 没这个产品时多痛
[10-22s] 解法 — 实际操作流程,3 步以内
[22-28s] 效果 — 直观展示成果(数据/对比/截图)
[28-30s] CTA — 网址 / 下载 / GitHub
```

**总长不超过 60 秒**。互联网上 50% 的观众在 6 秒内就跳走。

---

## 三、内容设计原则

### 钩子的 5 种打开方式
1. **反差**:"以前要 30 分钟,现在 30 秒"
2. **痛点提问**:"还在手写 SQL?"
3. **极端结果**:"我们用它做了一个 X"
4. **悬念**:"试试不写代码做这件事"
5. **数据**:"这个组件被复制了 1 万次"

### 解法呈现的 3 个动作
- **打开**(产品/页面)
- **操作**(关键步骤,2-3 个动作)
- **看见结果**(明显的视觉变化)

不要展示**配置过程**(注册、登录、安装) — 用片头字幕 / 跳过即可。

### 效果展示
- **前后对比**:同一画面分屏
- **数字**:大字号 + 动画(Before 30s / After 3s)
- **真实场景**:不要假数据(假数据骗不了人)

---

## 四、录屏 vs 程序化生成

### 录屏(asciinema / OBS / QuickTime + iMovie)
适合:
- 真实操作流程
- 个人项目快速产出
- 一次性 demo

工具:
- macOS:QuickTime / Loom
- 终端:asciinema(可重放,体积小)
- 跨平台:OBS

### 程序化生成(remotion)
适合:
- 需要参数化(同一模板、不同数据)
- 需要 CI 自动生成(每次发版自动出 demo)
- 需要高质量动效
- 多语言版本(同一模板换字幕)

remotion 的杀手特性:
- React 组件 = 视频帧
- 时间轴用 `useCurrentFrame()`
- Lambda 云渲染(并行加速)
- 可嵌入 Player 让用户预览

---

## 五、remotion 最小可运行示例

```tsx
// src/Demo.tsx
import { interpolate, useCurrentFrame } from 'remotion';

export const Demo = ({ title }: { title: string }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);

  return (
    <div style={{
      flex: 1,
      backgroundColor: '#0a0a0a',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      opacity,
    }}>
      <h1 style={{ color: 'white', fontSize: 80 }}>{title}</h1>
    </div>
  );
};

// src/Root.tsx
import { Composition } from 'remotion';
import { Demo } from './Demo';

export const Root = () => (
  <Composition
    id="Demo"
    component={Demo}
    durationInFrames={150} // 30fps × 5s = 150 帧
    fps={30}
    width={1920}
    height={1080}
    defaultProps={{ title: 'Hello' }}
  />
);
```

启动:`npx remotion preview`,渲染:`npx remotion render`。

---

## 六、Demo 录制工作流(集成到 design-dev-flow)

### 选项 A:轻量录屏(推荐 80% 项目)
1. 准备好真实数据 + 已部署版本
2. 用 QuickTime / OBS 录 60 秒原始素材
3. iMovie 剪到 30 秒,加字幕 + 钩子画面
4. 导出 mp4 + 转 gif(给 README)

### 选项 B:remotion 程序化(推荐数据驱动项目)
1. 设计 storyboard(每 3-5 秒一个场景)
2. 用 remotion 写组件
3. `npx remotion render`(本地或 Lambda)
4. 接入 CI(每次发版自动生成最新 demo)

### 选项 C:混合(技术演示项目)
1. asciinema 录终端操作
2. 用 [asciicast2gif](https://github.com/asciinema/asciicast2gif) 转 gif
3. 嵌入 README 顶部

---

## 七、Demo 元素清单(自检)

发布前检查:

- [ ] 有钩子(前 3 秒能让人停下)
- [ ] 有字幕(60% 的人静音看)
- [ ] 不超过 60 秒
- [ ] 关键操作可见(不被 cursor 挡住)
- [ ] 没有真实账号信息泄露(邮箱、token、URL)
- [ ] 字体/颜色与产品 brand 一致
- [ ] 有清晰 CTA(GitHub URL / 网址)
- [ ] mp4 + gif 两个格式都有
- [ ] gif 不超过 5MB(GitHub README 限制)

---

## 八、文件命名 / 存放约定

```
docs/
└── demo/
    ├── hero.mp4        # README 顶部用
    ├── hero.gif        # README 备用
    ├── login.gif       # 登录子流程
    ├── feature-x.mp4   # 单个特性介绍
    └── README.md       # 每个 demo 的拍摄说明(如何复现)
```

`docs/demo/README.md` 模板:
```md
## hero.mp4
- 时长: 30s
- 录制工具: remotion
- 数据源: docs/demo/hero-data.json
- 复现: cd docs/demo && npx remotion render Demo hero.mp4

## login.gif
- 时长: 6s
- 录制工具: QuickTime → iMovie → ezgif.com
- 复现: 跟 docs/demo/login-script.md 操作
```

---

## 九、不要做的事

- ❌ **录 5 分钟说"精剪 30 秒"**:精剪 90% 项目都没做完,不如一开始就限时
- ❌ **加复杂转场**:观众想看产品,不是看你的剪辑
- ❌ **用 stock 音乐**:版权风险,不如静音 + 字幕
- ❌ **演员表情包乱入**:除非品牌定位就是这样
- ❌ **demo 跟实际产品差异巨大**:被人发现就是诈骗(不是夸张)

---

## 十、与其他工具协作

| 工具 | 何时用 |
|------|--------|
| QuickTime / OBS | 真实操作录屏 |
| asciinema | 终端类项目 |
| Remotion | 数据驱动 / CI 集成 |
| ScreenStudio / Tella | 商业精修(付费但快) |
| ezgif.com | mp4 → gif 转换 |
| ffmpeg | 命令行处理(剪、压、拼) |

简单原则:**优先用最少工具**。能 QuickTime 搞定就别上 remotion。
