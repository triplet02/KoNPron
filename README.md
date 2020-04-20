# KoNPron
  
<img src="https://img.shields.io/badge/License-MIT-yellow"> <img src="https://img.shields.io/badge/contributors-welcome-yellowgreen">  
  
<img src="https://user-images.githubusercontent.com/53908830/79735575-7227c080-8333-11ea-9917-1f430bb4f3f2.png" width=500>  
  
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
공일공 일이삼사 오율칠팔로 전화해
오만원만 빌려줘봐. 다음달 십일까지 줄게.
```

## Troubleshoots and Contributing
If you have any questions, bug reports, and feature requests, please [open an issue](github.com/triplet02/KoNPron/issues) on Github.
or Contacts triplet02@naver.com please.

I appreciate any kind of feedback or contribution. Feel free to proceed with small issues like bug fixes, documentation improvement. For major contributions and new features, please discuss with the collaborators in corresponding issues.
