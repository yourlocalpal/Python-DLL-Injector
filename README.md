# Python-DLL-Injector

![Capture python](https://github.com/yourlocalpal/Python-DLL-Injector/assets/118146578/f0989dab-3170-4bf7-81a5-b796de6dba90)

Uses loadlibrarya function from win32: https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibrarya

all libraries that i used present on windows. you don't have to install anything to run it. other than python.

- Use PID to find process.
- Ensure you know if its 32bit or 64bit on target PID
- Inject 32bit or 64bit dll (I verified it works.)
