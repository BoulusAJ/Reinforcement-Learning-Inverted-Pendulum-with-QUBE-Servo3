/* Include files */

#include "ClosedLoopSystem_PID_Exp_python_block_2_cgxe.h"
#include "m_uZdi31gtSmAfYTvQm3xAoF.h"

unsigned int cgxe_ClosedLoopSystem_PID_Exp_python_block_2_method_dispatcher
  (SimStruct* S, int_T method, void* data)
{
  if (ssGetChecksum0(S) == 982582125 &&
      ssGetChecksum1(S) == 21952705 &&
      ssGetChecksum2(S) == 1468695306 &&
      ssGetChecksum3(S) == 3951138098) {
    method_dispatcher_uZdi31gtSmAfYTvQm3xAoF(S, method, data);
    return 1;
  }

  return 0;
}
