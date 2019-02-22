def wordLadder(beginWord, endWord, wordList):
    abc = ["a","e","i","o","u"]
    beginWord_Len = len(beginWord)
    endword_Len = len(endWord)
    orden = []
    for letra in beginWord:
        print letra
        for i in abc:
            if letra.lower() == i:
                orden.append(beginWord[letra])#VOCALES
                break
            else:
                if i == 'u':
                    #orden.append(1)#NOVOCALES
                    break
    
    print orden

        
                
            
wordLadder("hit","cog",["hot", "dot", "dog", "lot", "log", "cog"])    
