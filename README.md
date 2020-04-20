# KoNPron
  
<img src="https://img.shields.io/badge/License-MIT-yellow"> <img src="https://img.shields.io/badge/contributors-welcome-yellowgreen">  
  
<img src="https://user-images.githubusercontent.com/53908830/79735946-06922300-8334-11ea-98ea-cf11f2373ce7.png" width=500>  
  
숫자표기를 한국어 발음전사로 변환해주는 파이썬 패키지입니다.  
  
KoNPron is a Python package that converts numeric expressions into Korean phonetic transcription.
  
## How to use
  
* Example

```python
example1 = '010-1234-5678로 전화해'
example2 = '50,000원만 빌려줘봐. 다음달 10일까지 줄게.'
  
kpr = KoNPron()
converted1 = kpr.convert(example1)
converted2 = kpr.convert(example2)

print(converted1)
print(converted2)
```
* Output
```
공일공 일이삼사 오육칠팔로 전화해
오만원만 빌려줘봐. 다음달 십일까지 줄게.
```

## Troubleshoots and Contributing
If you have any questions, bug reports, and feature requests, please [open an issue](github.com/triplet02/KoNPron/issues) on Github,   
or Contact by triplet02@naver.com please.

I appreciate any kind of feedback or contribution. Feel free to proceed with small issues like bug fixes, documentation improvement. For major contributions and new features, please discuss with the collaborators in corresponding issues.

## License
```
MIT License

Copyright (c) 2020 triplet02

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
