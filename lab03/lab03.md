# Prompt Engineering Process

## attempt 1
#### Intention
>What is the improvement that you intend to make?

   I am trying to get the model to work with the minimum amount of tokens. The unrecorded attempt before this the I set the number of tokens to 10. The model proceeded to not work for some uknown reason. 

#### Action/Change
>Why do you think this action/change will improve the agent?

    I set the the number of tokens to 50, so the model will have more tokens to respond back to me.

#### Result
>What was the result?

    The LLM could successfully talk back in a shorter ammount of time compared to 100 tk's.

#### Reflection/Analysis of the result. 
>Why do you think it did or did not work?

    It did work. It was faster than 100 tk's.



## attempt 2
#### Intention
>What is the improvement that you intend to make?

    I addes a system prompt, telling the LLM that it was a charcater names 'Aku' and that its job was to create the most absurd DND campagin of all time. I tried to shape its responses by telling it to tell the user what it was writing and at what time so the story did not get confusing. Like tell it to write story segments with "STORY:{infomation in here}" or "ITEM:{infomation in here}"

#### Action/Change
>Why do you think this action/change will improve the agent?

   The agent will begin generating a DND story, hopefully, with a way of writing that matches a story-telling-like way instead of being very blunt. Additionally it will specify what it its writing, like the story or dialouge. Also the way the actions are formatted will hopefully fit the model like how regular prompts do.

#### Result
>What was the result?

    All the categories were there, but some of them were not generated with content, others seemed to be repeated and some of the content seems to be unrelated to the category.
   
#### Reflection/Analysis of the result. 
>Why do you think it did or did not work?

    It worked in the sense it generated the categories, but the content was a bit confused. More specifications will be needed to get the model to be coherent.





## attempt 3
#### Intention
>What is the improvement that you intend to make?

    In the previous attempt when I asked the model why it was messing up I got a hint that it liked **Dialouge**, **STORY** header format better compared to the json-like format. So I changed the system prompt to include that format and was more specific what goes under those segments.

#### Action/Change
>Why do you think this action/change will improve the agent?

   The agent added itself to the story, which is partially what I wanted. The Segments have become much more distinct and are now all the same format and do not have any weird capitolization like in the last attempt.
    
#### Result
>What was the result?

    All categories were successfully generated and were coherent. it was confusing who was talking, and what an item actually was. 

#### Reflection/Analysis of the result. 
>Why do you think it did or did not work?

   The categories were succsesfully generated with text that was coherent enough to call it a succsess. Though it treated every category like it was a passage in a book, so like for the ITEM categories that made it more confusing, I think specifying a writing stle for eachcategoy would be beneficial.


## attempt 4
#### Intention
>What is the improvement that you intend to make?

   I did not change the sys prompt I just changed the way I started talking to the model where I just said "just testing, make something short and quick."

#### Action/Change
>Why do you think this action/change will improve the agent?

   I wanted to see how the output would change if there was basically no specifications from the user.
    

#### Result
>What was the result?

    The model started generting the start to a whole story instead of like in the middle of a story like in the other ones. 

#### Reflection/Analysis of the result. 
>Why do you think it did or did not work?

    One of my issues is that it starts the story off in the middle of something, not with a definitive start, more like if you flipped to a random page in a book. Introducing a intro prompt will be beneficial.



## attempt 5
#### Intention
>What is the improvement that you intend to make?

  Added more clarity to the system prompt because its just putting whatever under each header.

#### Action/Change
>Why do you think this action/change will improve the agent?

    Im specifying like what it cant say now. It may NOT use any other headers and must stick to the framework im trying to get it to make. I added In the specification for Scene headers  'in the style of steven king' so that it may get the hint that it should be writing a story. 

#### Result
>What was the result?

    The model is inserting itself, and its trying to solve a system of equations? Its doing matrix solving or something. Why? Its also adding its own titles: "**WITING**", "**DIALOSONG**", ect. 


#### Reflection/Analysis of the result. 
>Why do you think it did or did not work?

    Im going to try to limit its behavior ny telling it in the sys prompt what it can't do, making a framework it has to work around.




## attempt 6
#### Intention
>What is the improvement that you intend to make?

    Added stuff the AI could not do. Made some of the descriptions into a list format so it does not do more that what is in the list and for what it should do and in what order. Specified D&D as Dungeons and Dragons. Told it that it should be writing a story that is interesting. I also added 'writing' prompts to dialouge header: "make it in the style of quinten tarentino".

#### Action/Change
>Why do you think this action/change will improve the agent?
    
    I think that adding a list of items to complete will make sure the ai does each step. Telling the AI what to do is much more of a specification that what I want it to do. Eliminating what I want it to do. I also added many more 
    
#### Result
>What was the result?

    It started numbering dialouges and scenes, I think its now more like a movie script than a like an entry because I put a bunch of "make it in the style of steven king" and "make it in the style of quinten tarentino"

#### Reflection/Analysis of the result. 
>Why do you think it did or did not work?

    Im gona remove the "in the style of" prompts they do not work and just confuse the model and turn its responses into a movie script
    
## attempt 7
#### Intention
>What is the improvement that you intend to make?

    Added a prompt to the messages with the role 'setting' inorder to try to force the ai to stay in the context of dungeons and dragons

       I attempted to add another systen prompt that tells the ai the setting we're in

      {
      'role': 'system', 
      'content' : 'The setting is a classical fantasy setting with various mid-evil inspired tropes from the \
        Dungeons and Dragons theme.'
   },
 
#### Action/Change
>Why do you think this action/change will improve the agent?

    This will force it to atleast start in a d&d context.

#### Result
>What was the result?
    It broke :(

#### Reflection/Analysis of the result. 
>Why do you think it did or did not work?  
    I guess you can only have one system prompt else the model gets confused, locks ups and cant do anything.




## attempt 8
#### Intention
>What is the improvement that you intend to make?
    I want to add choices, there the agent prompts 1-4 choices.

 
#### Action/Change
>Why do you think this action/change will improve the agent?

    Because it will add some easy user input and can force the ai to stick to something specific

#### Result
>What was the result?

    It listed choices, but when I picked one it bascially ignored me and skipped it.

#### Reflection/Analysis of the result. 
>Why do you think it did or did not work?

   Looking at its thinking outputs it seems like it sees that I picked a choice, but it just continues with whatever it was thinking about in its previous last segment. It keeps takling about birds and creatures with dark fingers!
   additionally, the dialouge is like not dialouge.

## overall goal
    I was trying to make it so that it would segment the output based on **headers** then I could segment up the output and put to use the data in reporompting the model. Because it seems to forget alot. However I cant get it to spit out a consistent format. So that is why I have Regex and stuff imported.


