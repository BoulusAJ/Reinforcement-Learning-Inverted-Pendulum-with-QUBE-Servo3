/* Include files */

#include "ClosedLoopSystem_PID_Exp_python_block_cgxe.h"
#include "m_yWqzPSpmRagDnAB9dbEQQG.h"

unsigned int cgxe_ClosedLoopSystem_PID_Exp_python_block_method_dispatcher
  (SimStruct* S, int_T method, void* data)
{
  if (ssGetChecksum0(S) == 207153531 &&
      ssGetChecksum1(S) == 1881781368 &&
      ssGetChecksum2(S) == 2887545974 &&
      ssGetChecksum3(S) == 819318139) {
    method_dispatcher_yWqzPSpmRagDnAB9dbEQQG(S, method, data);
    return 1;
  }

  return 0;
}
