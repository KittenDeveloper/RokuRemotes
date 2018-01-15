//Compiled with VS2017
//Command:cl RokuRemote.c user32.lib ws2_32.lib
#include <winsock2.h>
#include <windows.h>
#include <stdlib.h>
#include <tchar.h>
#include <string.h>
#define STR_EXPAND(tok) #tok
#define STR(tok) STR_EXPAND(tok)
#define ERR_BOX MessageBoxA(NULL, STR(Error near line: __LINE__ Check error code for details), NULL, MB_OK); 
char *discoverRokus()
{
	char *recvBuffer=malloc(sizeof(char)*218);
	int sockaddr_in_size=sizeof(struct sockaddr_in);
	char ssdpMessage[]="M-SEARCH * HTTP/1.1\nHost: 239.255.255.250:1900\nMan: \"ssdp:discover\"\nST: roku:ecp\n\n";
	WSADATA wsa;
	SOCKET s;
	if(WSAStartup(0x0101, &wsa)){ERR_BOX; exit(WSAGetLastError());}
	if((s=socket(AF_INET, SOCK_DGRAM, 0))==INVALID_SOCKET){ERR_BOX; exit(WSAGetLastError());}
	struct sockaddr_in server;
	memset((void *)&server, '\0', sizeof(struct sockaddr_in));
	server.sin_family=AF_INET;
	server.sin_port=htons(1900);
	server.sin_addr.S_un.S_addr= inet_addr("239.255.255.250");
	if(sendto(s, ssdpMessage, (int)strlen(ssdpMessage)+1, 0, (struct sockaddr*)&server, sizeof(struct sockaddr_in))==-1)
	{
		ERR_BOX; exit(WSAGetLastError());
	}
	if(recvfrom(s, (char*)&recvBuffer, (int)sizeof(recvBuffer), 0, (struct sockaddr*)&server, &sockaddr_in_size)<0)
	{
		ERR_BOX; exit(WSAGetLastError());
	}
	closesocket(s);
	WSACleanup();
	return recvBuffer;
}
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
	discoverRokus();
	printf("%s, %d", recvBuffer, strlen(recvBuffer)+1);
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