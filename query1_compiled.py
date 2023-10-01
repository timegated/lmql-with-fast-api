import lmql
@lmql.compiled_query(output_variables=["INT_VALUE", "STRING_VALUE"])
async def query(context=None):
   yield lmql.runtime_support.context_call("set_model", 'openai/text-davinci-003')
   yield lmql.runtime_support.context_call("set_decoder", 'argmax', )
   # where
   intm0 = lmql.ops.Lt([lmql.ops.LenOp([lmql.ops.TokensOp([lmql.runtime_support.Var('INT_VALUE')])]), 2])
   intm1 = lmql.ops.AndOp([
     lmql.ops.StopBeforeOp([lmql.runtime_support.Var('STRING_VALUE'), '"']),
     lmql.ops.IntOp([lmql.runtime_support.Var('INT_VALUE')]),
     intm0
   ])
   yield lmql.runtime_support.context_call("set_where_clause", intm1)
   # prompt
   (yield lmql.runtime_support.interrupt_call('query', f"""\nWrite a summary of Led Zeppelin, the 1970's rock band:\n{{\n  "name": "[STRING_VALUE]",\n  "age": [INT_VALUE],\n  "top_songs": [[\n     "[STRING_VALUE]",\n     "[STRING_VALUE]"\n  ]]\n}}\n"""))
   INT_VALUE = (yield lmql.runtime_support.context_call('get_var', 'INT_VALUE'))
   STRING_VALUE = (yield lmql.runtime_support.context_call('get_var', 'STRING_VALUE'))
   yield ('result', (yield lmql.runtime_support.context_call("get_return_value", ())))
