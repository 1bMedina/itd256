# Caching

- Caching is critical when it comes to the architecture of memory. It underlies everything from the layout of the processor chips at the millimeter scale to the geography of the global internet. 

- **Memory hierarchy can be seen in libraries. Instead of going back to the library many times to see the same book, you can just check it out.** 

- **The ability to check out many books and work from home, is almost just as good as if you had every book in the library available at your desk. The more trips back to the library, the slower things go, and the less useful your desk really is.**

- The idea of keeping around pieces of information that you refer to frequently is so powerful that it is used in every aspect of computation.

- Many things have caches; processors, hard drives, operating systems, web browsers, and even the servers that deliver content to the web browsers.

- Computer scientists best defense against hitting a memory wall is to create a more elaborate hierarchy: cache for cache for cache and so on. 

- If you want to make room to store anything else once a cache fills up, you do something called cache replacement or cache eviction. 

- IBM played an early role in developing caches.

- Caches need an algorithm that is progressively overwritten to make room for new things. 

- **Just having a cache makes a system more efficient, no matter how it is maintained.**

- **Libraries themselves, with their various sections and storage facilities are a great example of a memory hierarchy with multiple levels.**

- **Due to this they face many caching problems; which books to put in the limited display case, which to keep in their stacks, and which to move to offsite storage.**

- **Most libraries use LRU as a way of deciding which books get moved offsite.**

- **Many libraries use different kinds of caches, for example the Moffit Undergraduate Library showcases the most recently acquired books. This is a kind of FIFO cache.**

- Companies like Amazon use caching. 

- Caching shows us that memory involves unavoidable tradeoffs and a certain zero-sumness. 
