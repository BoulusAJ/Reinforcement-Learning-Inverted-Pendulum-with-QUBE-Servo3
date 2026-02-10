#ifndef __yWqzPSpmRagDnAB9dbEQQG_h__
#define __yWqzPSpmRagDnAB9dbEQQG_h__

/* Include files */
#include "simstruc.h"
#include "rtwtypes.h"
#include "multiword_types.h"
#include "slexec_vm_zc_functions.h"
#include "slexec_vm_simstruct_bridge.h"
#include "sl_sfcn_cov/sl_sfcn_cov_bridge.h"

/* Type Definitions */
#ifndef typedef_InstanceStruct_yWqzPSpmRagDnAB9dbEQQG
#define typedef_InstanceStruct_yWqzPSpmRagDnAB9dbEQQG

typedef struct {
  SimStruct *S;
  PyObject *namespaceDict;
  PyGILState_STATE GIL;
  void *emlrtRootTLSGlobal;
  real_T *u0;
  boolean_T *u1;
  real_T *b_y0;
  real_T *b_y1;
  real_T *y2;
  real_T *y3;
  real_T *y4;
  real_T *y5;
} InstanceStruct_yWqzPSpmRagDnAB9dbEQQG;

#endif                                 /* typedef_InstanceStruct_yWqzPSpmRagDnAB9dbEQQG */

/* Named Constants */

/* Variable Declarations */

/* Variable Definitions */

/* Function Declarations */

/* Function Definitions */
extern void method_dispatcher_yWqzPSpmRagDnAB9dbEQQG(SimStruct *S, int_T method,
  void* data);

#endif
