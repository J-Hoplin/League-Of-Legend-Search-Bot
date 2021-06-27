Discord Bot : League of Legend player information search bot
===


***
1 . Discord.py Version : 1.0.0(Rewrite Version)

2 . Language : Python3

3 . What for? : To make able to see summoner's information URL, Rank Info, Most Champion with using command

4 . Warning  : This Application is only available for South Korea. 
***
- Patch Note 20200503
    
    - Issue : https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/issues/2

    - Bug Fix : In [Base-Version](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/Base-Version/lolSearchbot.py) line number 107, 108 this code is written to get rank medal image only. But it get banner images also. This line change like this.

    ```python
    Medal = bs.find('div', {'class': 'ContentWrap tabItems'})
    RankMedal = Medal.findAll('img', {'src': re.compile('//[a-z]-[A-Za-z].[A-Za-z].[A-Za-z]/[A-Za-z]/[A-Za-z]/[a-z0-9_]*.png')})
    ```

    - Really thanks to [moonjy1120](https://github.com/moonjy1120) finding this bug :D

- Patch Note 20200504

    - Issue : https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/issues/3

    - Main Content : Algorithm Change. Now it's little bit more faster than before

    - Bug Fix : In patch Note 20200503 I change code like this in consideration of maintenance.

    ```python
    Medal = bs.find('div', {'class': 'ContentWrap tabItems'})
    RankMedal = Medal.findAll('img', {'src': re.compile('//[a-z]-[A-Za-z].[A-Za-z].[A-Za-z]/[A-Za-z]/[A-Za-z]/[a-z0-9_]*.png')})
    ```

    - But depending on your PC's configuration or OS platform, Python can't recognize white blank of 'ContentWrap tabItems'. To de fine more clearly I change variable 'Medal' like this.
    
    ```python
    Medal = bs.find('div', {'class': 'SideContent'})
    RankMedal = Medal.findAll('img', {'src': re.compile('\/\/[a-z]*\-[A-Za-z]*\.[A-Za-z]*\.[A-Za-z]*\/[A-Za-z]*\/[A-Za-z]*\/[a-z0-9_]*\.png')})
    ```


***

- How to Use?

    - !롤전적 (player nickname) : Print simple player's information from op.gg
    

    ![img](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/img/1.PNG?raw=true)

    ![img](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/img/2.PNG?raw=true)
    
    ![img](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/img/3.PNG?raw=true)
    
    ![img](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/img/4.PNG)
