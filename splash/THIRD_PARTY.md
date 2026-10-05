# Third-Party Licenses

## React Bits

**Repository:** https://github.com/DavidHDev/react-bits
**License:** MIT
**Author:** DavidHDev

### Components Used

- `Backgrounds/DotGrid` - Animated dot grid background
- `TextAnimations/DecryptedText` - Text decryption animation
- `TextAnimations/CountUp` - Numeric counter animation
- `TextAnimations/TrueFocus` - Cycling text focus effect
- `Animations/StarBorder` - Animated star border effect
- `Components/Stack` - Draggable card stack; used for the mystery deck's fanned
  "peek" of the upcoming cards. Copied verbatim from
  `src/content/Components/Stack/{Stack.jsx,Stack.css}` on `main`
  (https://github.com/DavidHDev/react-bits/blob/main/src/content/Components/Stack/Stack.jsx).
  It is a send-to-back / auto-cycle gallery; the deck's controlled navigation (prev/next
  buttons, arrow keys, the "card N of 6" counter, the closing panel, and the per-card
  inspect → commit → reveal flow) lives in `src/components/Deck.jsx`, and the reveal flip is
  a plain-CSS 3D transform (not motion). Uses the `motion` (framer-motion) package already
  a dependency of this app, so it adds no new dependency.

All components are used under the MIT License.

### React Bits License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
