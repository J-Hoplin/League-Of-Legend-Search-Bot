Discord Bot : League of Legend player information search bot
===

**봇 소스코드를 가져가서 쓰시되, 출처를 꼭 밝히고 쓰시길 바랍니다**

***
1 . Discord.py Version : 1.0.0(Rewrite Version)

2 . Language : Python3

3 . What for? : To make able to see summoner's information URL, Rank Info, Most Champion with using command

4 . Warning  : This Application is only available for South Korea. I'm gonna make other countries' server able to use it.
***
- Patch Note 20200503
    
    - Issue : https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/issues/2

    - Bug Fix : In [Base-Version](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/Base-Version/lolSearchbot.py) line number 107, 108 it also get banner images. This line change like this.

    ```python
    Medal = bs.find('div', {'class': 'ContentWrap tabItems'})
        RankMedal = Medal.findAll('img', {'src': re.compile('//[a-z]-[A-Za-z].[A-Za-z].[A-Za-z]/[A-Za-z]/[A-Za-z]/[a-z0-9_]*.png')})
    ```

    - Really thanks to [moonjy1120](https://github.com/moonjy1120) for finding this bug :D

***

- How to Use?

    - !롤전적 (player nickname) : Print simple player's information from op.gg
    

    ![img](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/img/1.PNG?raw=true)

    ![img](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/img/2.PNG?raw=true)
    
    ![img](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/img/3.PNG?raw=true)
    
    ![img](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/img/4.PNG)
