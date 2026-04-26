from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic:str) ->dict:
    state = {}

    #step 1: search
    print("\n" + "="*80)
    print(f"[bold green] Search Agent: Finding sources for '{topic}'[/bold green]")
    print("="*80 + "\n")

    search_agent = build_search_agent()
    search_result= search_agent.invoke({
        "messages":[("user", f"Find recent, reliable and detailed information on {topic}.")]
    })
    state['search_results'] = search_result['messages'][-1].content

    print("\n search result ", state['search_results'])

    #step2 reader agent
    print("\n" + "="*80)
    print("[bold green] Reader Agent: Reading web pages...[/bold green]")
    print("="*80 + "\n")

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })
    state['scraped_content'] = reader_result['messages'][-1].content

    print("\nscraped content: \n", state['scraped_content'])

    #step3 writer agent
    print("\n" + "="*80)
    print("[bold green]🤖 Writer Agent: Writing research report...[/bold green]")
    print("="*80 + "\n")

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n",state['report'])

    #step4 critic agent
    print("\n" + "="*80)
    print("[bold green]🤖 Critic Agent: Reviewing research report...[/bold green]")
    print("="*80 + "\n")

    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state

if __name__=="__main__":
    topic= input("\n Enter the research topic :")
    run_research_pipeline(topic)
