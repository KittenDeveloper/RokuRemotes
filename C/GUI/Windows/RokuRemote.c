//Compiled with VS2017
//Command:cl RokuRemote.c user32.lib ws2_32.lib
#include <winsock2.h>
#include <windows.h>
#include <stdlib.h>
#include <tchar.h>
LRESULT CALLBACK WndProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
	PAINTSTRUCT ps;
	HDC hdc;
	switch (uMsg)
	{
		case WM_PAINT:
			hdc = BeginPaint(hWnd, &ps);
			EndPaint(hWnd, &ps);
			break;
		case WM_DESTROY:
			PostQuitMessage(0);
			break;
		default:
			return DefWindowProc(hWnd, uMsg, wParam, lParam);
			break;
	}
	return 0;
}
int main(int argc, char **argv)
{
	TCHAR szWindowClass[]= _T("RokuRemote");
	TCHAR szTitle[]= _T("Roku Remote");
	WNDCLASSEX wc;
	wc.cbSize=sizeof(WNDCLASSEX);
	wc.style= CS_HREDRAW|CS_VREDRAW;
	wc.lpfnWndProc=WndProc;
	wc.cbClsExtra=0;
	wc.cbWndExtra=0;
	wc.hInstance=GetModuleHandleW(0);
	wc.hIcon=LoadIcon(wc.hInstance, IDI_APPLICATION);
	wc.hCursor=LoadCursor(NULL, IDC_ARROW);
	wc.hbrBackground=(HBRUSH)(COLOR_WINDOW+1);
	wc.lpszMenuName=NULL;
	wc.lpszClassName=szWindowClass;
	wc.hIconSm=LoadIcon(wc.hInstance, IDI_APPLICATION);
	
	if (!RegisterClassEx(&wc))
	{
		MessageBoxA(NULL, "Couldn't Register Window", NULL, MB_OK);
		return 1;
	}
	
	HWND hWnd=CreateWindow(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 150, 300, NULL, NULL, wc.hInstance, NULL);
	if(!hWnd)
	{
		MessageBox(NULL, "Couldn't Create Window", NULL, MB_OK);
		return 1;
	}
	ShowWindow(hWnd, SW_SHOW);
	UpdateWindow(hWnd);
	MSG msg;
	while (GetMessage(&msg, NULL, 0, 0))
	{
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}
	return (int) msg.wParam;
}