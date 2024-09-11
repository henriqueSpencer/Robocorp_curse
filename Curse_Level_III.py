""" 
 This is the third level of the curse
 
 Problema a ser resolvido:
    - Your robot will produce business data from raw input data and then consume that data in small chunks - work items.
    - Split your robot code into multiple logical pieces
    - Extract, Transform, Load - (ETL)
    - Integrating the road traffic fatality rate API ---> insurance sales system
    - Producer-consumer pattern (allows you to track the status of individual requests and mitigates the risk of everything falling apart)


    -producer.py:
    consumer.py

┌──────────┐   ┌────────────┐   ┌──────────┐   ┌─────────────────┐
│ Producer │ → │ Work items │ → │ Consumer │ → │ Done work items │ → 💰
└──────────┘   └────────────┘   └──────────┘   └─────────────────┘
                                      ↓                  ↑
                       ┌───────────────────┐             ↑
                       │ Failed work items │ → → Retry → ↑
                       └───────────────────┘

"""
