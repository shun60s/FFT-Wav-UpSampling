# FFT-Wav-UpSampling
A converter of audio wav file samplimg rate to 2 times by FFT method  
FFT法を使って　音楽などのWAVファイルのサンプリング周波数を2倍にする。  
There is a new version, [FFT-Wav-UpSampling2](https://github.com/shun60s/FFT-Wav-UpSampling2/), in github repository.  

## Document
See FFT-UpSamplingu.pdf  
FFT-UpSamplingu.pdfを見てください。  

## Usage
Specify input/output wav file name in the content.
* input/output width 16bit, stereo
```
python sample16bitout.py
```
* input width 16bit/output width 24bit, stereo
```
python sample24bitout.py
```

## License
 Regarding to wavio.py, follow the license wrtten in the content.

## Disclaimer
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
