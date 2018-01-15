//Library for extracting from some of the html/xml bits
#include <string.h>
char* findWord(char *base, char *search)
{
	int offset=0;
	int currentPos;
	if(strlen(search)<strlen(base))
	{
		while(offset<=strlen(base))
		{
			offset=strchr(base+offset, search[0])-base
			int i;
			for(i=0; i<strlen(search)-1; i++)
			{
				printf("%s", base+offset);
			}
		}
	}
	return -1;
}