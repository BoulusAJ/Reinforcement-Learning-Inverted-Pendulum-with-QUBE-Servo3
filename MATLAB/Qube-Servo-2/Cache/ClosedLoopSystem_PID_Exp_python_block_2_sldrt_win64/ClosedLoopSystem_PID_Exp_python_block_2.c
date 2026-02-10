/*
 * ClosedLoopSystem_PID_Exp_python_block_2.c
 *
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * Code generation for model "ClosedLoopSystem_PID_Exp_python_block_2".
 *
 * Model version              : 10.5
 * Simulink Coder version : 25.2 (R2025b) 28-Jul-2025
 * C source code generated on : Tue Feb 10 11:19:56 2026
 *
 * Target selection: sldrt.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Intel->x86-64 (Linux 64)
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "ClosedLoopSystem_PID_Exp_python_block_2.h"
#include "rtwtypes.h"
#include <stddef.h>
#include <string.h>
#include "rt_nonfinite.h"
#include "ClosedLoopSystem_PID_Exp_python_block_2_dt.h"

/* list of Simulink Desktop Real-Time timers */
const int SLDRTTimerCount = 1;
const double SLDRTTimers[2] = {
  0.005, 0.0,
};

/* Block signals (default storage) */
B_ClosedLoopSystem_PID_Exp_python_block_2_T
  ClosedLoopSystem_PID_Exp_python_block_2_B;

/* Block states (default storage) */
DW_ClosedLoopSystem_PID_Exp_python_block_2_T
  ClosedLoopSystem_PID_Exp_python_block_2_DW;

/* Real-time model */
static RT_MODEL_ClosedLoopSystem_PID_Exp_python_block_2_T
  ClosedLoopSystem_PID_Exp_python_block_2_M_;
RT_MODEL_ClosedLoopSystem_PID_Exp_python_block_2_T *const
  ClosedLoopSystem_PID_Exp_python_block_2_M =
  &ClosedLoopSystem_PID_Exp_python_block_2_M_;

/* Forward declaration for local functions */
static void ClosedLoopSystem_PID_Exp_python_block_2_setPythonPath(void);
static PyObject *ClosedLoopSystem_PID_Exp_python_block_2_getPyNamespaceDict(void);
static PyObject *ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalOut(real_T
  inputVal);
static void ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(PyObject
  *dict, char_T *key, real_T val);
static void ClosedLoopSystem_PID_Exp_python_block_2_PyXDecRef(PyObject *obj);
static void ClosedLoopSystem_PID_Exp_python_block_2_deleteLocalsFromPyNamespace
  (PyObject *originalNamespace, PyObject *modifiedNamespace);
static void ClosedLoopSystem_PID_Exp_python_block_2_execPyScript(char_T *script,
  PyObject *ns);
static PyObject *ClosedLoopSystem_PID_Exp_python_block_2_getPyDictVal(PyObject
  *dict, char_T *key);
static real_T ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalIn(PyObject
  *pyToMarshal);
static PyObject *ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalOut_fr
  (boolean_T arg0);
static void ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict_frd0igp
  (PyObject *dict, char_T *key, boolean_T val);
static void ClosedLoopSystem_PID_Exp_python_block_2_deleteDictItem(PyObject
  *dict, char_T *key);
static void ClosedLoopSystem_PID_Exp_python_block_2_execPyScript_fr(char_T
  *script, PyObject *ns);
static PyObject *namespaceDict;
static void ClosedLoopSystem_PID_Exp_python_block_2_setPythonPath(void)
{
  PyObject *sysPath;
  sysPath = PySys_GetObject("path");
  PyList_Append(sysPath, PyUnicode_FromString(""));
}

static PyObject *ClosedLoopSystem_PID_Exp_python_block_2_getPyNamespaceDict(void)
{
  return PyDict_Copy(PyModule_GetDict(PyImport_AddModule("__main__")));
}

static PyObject *ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalOut(real_T
  inputVal)
{
  return PyFloat_FromDouble(inputVal);
}

static void ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(PyObject
  *dict, char_T *key, real_T val)
{
  PyObject *pyObj;
  if (dict != NULL) {
    pyObj = ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalOut(val);
    PyDict_SetItemString(dict, key, pyObj);
    Py_DecRef(pyObj);
  }
}

static void ClosedLoopSystem_PID_Exp_python_block_2_PyXDecRef(PyObject *obj)
{
  if (obj != NULL) {
    Py_DecRef(obj);
  }
}

static void ClosedLoopSystem_PID_Exp_python_block_2_deleteLocalsFromPyNamespace
  (PyObject *originalNamespace, PyObject *modifiedNamespace)
{
  PyObject *key;
  PyObject *modifiedNamespaceKeys;
  Py_ssize_t i;
  Py_ssize_t numKeysInModifiedNs;
  modifiedNamespaceKeys = PyDict_Keys(modifiedNamespace);
  numKeysInModifiedNs = PyList_Size(modifiedNamespaceKeys);
  for (i = 0; i < numKeysInModifiedNs; i++) {
    key = PySequence_GetItem(modifiedNamespaceKeys, i);
    if ((PyDict_Contains(originalNamespace, key) == 0) && (PyModule_Check
         (PyDict_GetItem(modifiedNamespace, key)) == 0)) {
      PyDict_DelItem(modifiedNamespace, key);
    }

    Py_DecRef(key);
  }

  Py_DecRef(modifiedNamespaceKeys);
}

static void ClosedLoopSystem_PID_Exp_python_block_2_execPyScript(char_T *script,
  PyObject *ns)
{
  PyObject *codeObject;
  PyObject *originalNamespace;
  PyObject *unusedEvalResult;
  if (ns != NULL) {
    codeObject = Py_CompileString(script, "Python Code Block", 257);
    originalNamespace = PyDict_Copy(ns);
    unusedEvalResult = PyEval_EvalCode(codeObject, ns, ns);
    Py_DecRef(codeObject);
    ClosedLoopSystem_PID_Exp_python_block_2_PyXDecRef(unusedEvalResult);
    ClosedLoopSystem_PID_Exp_python_block_2_deleteLocalsFromPyNamespace
      (originalNamespace, ns);
    Py_DecRef(originalNamespace);
  }
}

static PyObject *ClosedLoopSystem_PID_Exp_python_block_2_getPyDictVal(PyObject
  *dict, char_T *key)
{
  PyObject *value;
  value = PyDict_GetItemString(dict, key);
  Py_IncRef(value);
  return value;
}

static real_T ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalIn(PyObject
  *pyToMarshal)
{
  return PyFloat_AsDouble(pyToMarshal);
}

static PyObject *ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalOut_fr
  (boolean_T arg0)
{
  return PyBool_FromLong(arg0);
}

static void ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict_frd0igp
  (PyObject *dict, char_T *key, boolean_T val)
{
  PyObject *pyObj;
  if (dict != NULL) {
    pyObj = ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalOut_fr(val);
    PyDict_SetItemString(dict, key, pyObj);
    Py_DecRef(pyObj);
  }
}

static void ClosedLoopSystem_PID_Exp_python_block_2_deleteDictItem(PyObject
  *dict, char_T *key)
{
  if (dict != NULL) {
    PyDict_DelItemString(dict, key);
    PyErr_Clear();
  }
}

static void ClosedLoopSystem_PID_Exp_python_block_2_execPyScript_fr(char_T
  *script, PyObject *ns)
{
  PyObject *codeObject;
  PyObject *originalNamespace;
  PyObject *unusedEvalResult;
  if (ns != NULL) {
    codeObject = Py_CompileString(script, "Python Code Block", 257);
    originalNamespace = PyDict_Copy(ns);
    unusedEvalResult = PyEval_EvalCode(codeObject, ns, ns);
    Py_DecRef(codeObject);
    ClosedLoopSystem_PID_Exp_python_block_2_PyXDecRef(unusedEvalResult);
    Py_DecRef(originalNamespace);
  }
}

/* Model output function */
void ClosedLoopSystem_PID_Exp_python_block_2_output(void)
{
  PyObject *tmp;

  /* Reset subsysRan breadcrumbs */
  srClearBC(ClosedLoopSystem_PID_Exp_python_block_2_DW.RealTimeSync_SubsysRanBC);

  /* PythonCode: '<Root>/Python Code1' incorporates:
   *  Constant: '<Root>/Constant5'
   *  Constant: '<Root>/Constant6'
   */
  ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(namespaceDict,
    "current", ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o5);
  ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict_frd0igp(namespaceDict,
    "enable", ClosedLoopSystem_PID_Exp_python_block_2_P.Constant6_Value);
  ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(namespaceDict, "fault",
    ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o6);
  ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(namespaceDict, "phi",
    ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o2);
  ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(namespaceDict,
    "phi_dot", ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o4);
  ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(namespaceDict, "theta",
    ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o1);
  ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(namespaceDict,
    "theta_dot", ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o3);
  ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(namespaceDict, "u",
    ClosedLoopSystem_PID_Exp_python_block_2_P.Constant5_Value);
  ClosedLoopSystem_PID_Exp_python_block_2_execPyScript(
    "from rl_qube.simulink.qube3_block import step_1, start\n#import time\n#time.sleep(3) # Sleep for 3 seconds\n\ntheta, phi, theta_dot, phi_dot, current, fault = step_1(u, enable)\n\n",
    namespaceDict);
  tmp = ClosedLoopSystem_PID_Exp_python_block_2_getPyDictVal(namespaceDict,
    "current");

  /* PythonCode: '<Root>/Python Code1' */
  ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o5 =
    ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalIn(tmp);

  /* PythonCode: '<Root>/Python Code1' */
  Py_DecRef(tmp);
  tmp = ClosedLoopSystem_PID_Exp_python_block_2_getPyDictVal(namespaceDict,
    "fault");

  /* PythonCode: '<Root>/Python Code1' */
  ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o6 =
    ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalIn(tmp);

  /* PythonCode: '<Root>/Python Code1' */
  Py_DecRef(tmp);
  tmp = ClosedLoopSystem_PID_Exp_python_block_2_getPyDictVal(namespaceDict,
    "phi");

  /* PythonCode: '<Root>/Python Code1' */
  ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o2 =
    ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalIn(tmp);

  /* PythonCode: '<Root>/Python Code1' */
  Py_DecRef(tmp);
  tmp = ClosedLoopSystem_PID_Exp_python_block_2_getPyDictVal(namespaceDict,
    "phi_dot");

  /* PythonCode: '<Root>/Python Code1' */
  ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o4 =
    ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalIn(tmp);

  /* PythonCode: '<Root>/Python Code1' */
  Py_DecRef(tmp);
  tmp = ClosedLoopSystem_PID_Exp_python_block_2_getPyDictVal(namespaceDict,
    "theta");

  /* PythonCode: '<Root>/Python Code1' */
  ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o1 =
    ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalIn(tmp);

  /* PythonCode: '<Root>/Python Code1' */
  Py_DecRef(tmp);
  tmp = ClosedLoopSystem_PID_Exp_python_block_2_getPyDictVal(namespaceDict,
    "theta_dot");

  /* PythonCode: '<Root>/Python Code1' */
  ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o3 =
    ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalIn(tmp);

  /* PythonCode: '<Root>/Python Code1' */
  Py_DecRef(tmp);

  /* Gain: '<S2>/Gain' */
  ClosedLoopSystem_PID_Exp_python_block_2_B.Gain =
    ClosedLoopSystem_PID_Exp_python_block_2_P.Gain_Gain *
    ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o1;

  /* Gain: '<S3>/Gain' */
  ClosedLoopSystem_PID_Exp_python_block_2_B.Gain_h =
    ClosedLoopSystem_PID_Exp_python_block_2_P.Gain_Gain_n *
    ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o2;

  /* ToAsyncQueueBlock generated from: '<Root>/Python Code1' */
  {
    {
      double time = ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.t[0];
      void *pData = (void *)
        &ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o1;
      int32_T size = 1*sizeof(real_T);
      sendToAsyncQueueTgtAppSvc(3867142013U, time, pData, size);
    }
  }

  /* S-Function (sldrtsync): '<Root>/Real-Time Synchronization' */
  /* S-Function Block: <Root>/Real-Time Synchronization */
  {
    ClosedLoopSystem_PID_Exp_python_block_2_B.RealTimeSynchronization = 0;/* Missed Ticks value is always zero */
  }

  /* Outputs for Enabled SubSystem: '<S1>/Real-Time Sync' incorporates:
   *  EnablePort: '<S4>/Enable'
   */
  /* Constant: '<S1>/Synchronization' */
  if (ClosedLoopSystem_PID_Exp_python_block_2_P.Synchronization_Value > 0.0) {
    /* S-Function (sldrtsync): '<S4>/Real-Time Synchronization' */
    /* S-Function Block: <S4>/Real-Time Synchronization */
    {
    }

    srUpdateBC
      (ClosedLoopSystem_PID_Exp_python_block_2_DW.RealTimeSync_SubsysRanBC);
  }

  /* End of Constant: '<S1>/Synchronization' */
  /* End of Outputs for SubSystem: '<S1>/Real-Time Sync' */
}

/* Model update function */
void ClosedLoopSystem_PID_Exp_python_block_2_update(void)
{
  /* Update absolute time for base rate */
  /* The "clockTick0" counts the number of times the code of this task has
   * been executed. The absolute time is the multiplication of "clockTick0"
   * and "Timing.stepSize0". Size of "clockTick0" ensures timer will not
   * overflow during the application lifespan selected.
   * Timer of this task consists of two 32 bit unsigned integers.
   * The two integers represent the low bits Timing.clockTick0 and the high bits
   * Timing.clockTickH0. When the low bit overflows to 0, the high bits increment.
   */
  if (!(++ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.clockTick0)) {
    ++ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.clockTickH0;
  }

  ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.t[0] =
    ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.clockTick0 *
    ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.stepSize0 +
    ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.clockTickH0 *
    ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.stepSize0 * 4294967296.0;
}

/* Model initialize function */
void ClosedLoopSystem_PID_Exp_python_block_2_initialize(void)
{
  {
    PyObject *tmp;

    /* InitializeConditions for PythonCode: '<Root>/Python Code1' */
    Py_Initialize();
    ClosedLoopSystem_PID_Exp_python_block_2_setPythonPath();

    /* InitializeConditions for PythonCode: '<Root>/Python Code1' */
    namespaceDict = ClosedLoopSystem_PID_Exp_python_block_2_getPyNamespaceDict();
    ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(namespaceDict,
      "current", 0.0);
    ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(namespaceDict,
      "fault", 0.0);
    ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(namespaceDict, "phi",
      0.0);
    ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(namespaceDict,
      "phi_dot", 0.0);
    ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(namespaceDict,
      "theta", 0.0);
    ClosedLoopSystem_PID_Exp_python_block_2_assignToPyDict(namespaceDict,
      "theta_dot", 0.0);
    ClosedLoopSystem_PID_Exp_python_block_2_execPyScript(
      "from rl_qube.simulink.qube3_block import start\n\nstart(frequency=200, vlimit=2.0)\n",
      namespaceDict);
    tmp = ClosedLoopSystem_PID_Exp_python_block_2_getPyDictVal(namespaceDict,
      "current");

    /* InitializeConditions for PythonCode: '<Root>/Python Code1' */
    ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o5 =
      ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalIn(tmp);

    /* InitializeConditions for PythonCode: '<Root>/Python Code1' */
    Py_DecRef(tmp);
    tmp = ClosedLoopSystem_PID_Exp_python_block_2_getPyDictVal(namespaceDict,
      "fault");

    /* InitializeConditions for PythonCode: '<Root>/Python Code1' */
    ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o6 =
      ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalIn(tmp);

    /* InitializeConditions for PythonCode: '<Root>/Python Code1' */
    Py_DecRef(tmp);
    tmp = ClosedLoopSystem_PID_Exp_python_block_2_getPyDictVal(namespaceDict,
      "phi");

    /* InitializeConditions for PythonCode: '<Root>/Python Code1' */
    ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o2 =
      ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalIn(tmp);

    /* InitializeConditions for PythonCode: '<Root>/Python Code1' */
    Py_DecRef(tmp);
    tmp = ClosedLoopSystem_PID_Exp_python_block_2_getPyDictVal(namespaceDict,
      "phi_dot");

    /* InitializeConditions for PythonCode: '<Root>/Python Code1' */
    ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o4 =
      ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalIn(tmp);

    /* InitializeConditions for PythonCode: '<Root>/Python Code1' */
    Py_DecRef(tmp);
    tmp = ClosedLoopSystem_PID_Exp_python_block_2_getPyDictVal(namespaceDict,
      "theta");

    /* InitializeConditions for PythonCode: '<Root>/Python Code1' */
    ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o1 =
      ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalIn(tmp);

    /* InitializeConditions for PythonCode: '<Root>/Python Code1' */
    Py_DecRef(tmp);
    tmp = ClosedLoopSystem_PID_Exp_python_block_2_getPyDictVal(namespaceDict,
      "theta_dot");

    /* InitializeConditions for PythonCode: '<Root>/Python Code1' */
    ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o3 =
      ClosedLoopSystem_PID_Exp_python_block_2_PyObj_marshalIn(tmp);

    /* InitializeConditions for PythonCode: '<Root>/Python Code1' */
    Py_DecRef(tmp);
  }
}

/* Model terminate function */
void ClosedLoopSystem_PID_Exp_python_block_2_terminate(void)
{
  /* Terminate for PythonCode: '<Root>/Python Code1' */
  ClosedLoopSystem_PID_Exp_python_block_2_deleteDictItem(namespaceDict, "enable");
  ClosedLoopSystem_PID_Exp_python_block_2_deleteDictItem(namespaceDict, "u");
  ClosedLoopSystem_PID_Exp_python_block_2_execPyScript_fr(
    "from rl_qube.simulink.qube3_block import stop\n\nstop()\n", namespaceDict);
  Py_DecRef(namespaceDict);
}

/*========================================================================*
 * Start of Classic call interface                                        *
 *========================================================================*/
void MdlOutputs(int_T tid)
{
  ClosedLoopSystem_PID_Exp_python_block_2_output();
  UNUSED_PARAMETER(tid);
}

void MdlUpdate(int_T tid)
{
  ClosedLoopSystem_PID_Exp_python_block_2_update();
  UNUSED_PARAMETER(tid);
}

void MdlInitializeSizes(void)
{
}

void MdlInitializeSampleTimes(void)
{
}

void MdlInitialize(void)
{
}

void MdlStart(void)
{
  ClosedLoopSystem_PID_Exp_python_block_2_initialize();
}

void MdlTerminate(void)
{
  ClosedLoopSystem_PID_Exp_python_block_2_terminate();
}

/* Registration function */
RT_MODEL_ClosedLoopSystem_PID_Exp_python_block_2_T
  *ClosedLoopSystem_PID_Exp_python_block_2(void)
{
  /* Registration code */

  /* initialize non-finites */
  rt_InitInfAndNaN(sizeof(real_T));

  /* non-finite (run-time) assignments */
  ClosedLoopSystem_PID_Exp_python_block_2_P.RealTimeSynchronization_MaxMissedTicks
    = rtInf;

  /* initialize real-time model */
  (void) memset((void *)ClosedLoopSystem_PID_Exp_python_block_2_M, 0,
                sizeof(RT_MODEL_ClosedLoopSystem_PID_Exp_python_block_2_T));

  /* Initialize timing info */
  {
    int_T *mdlTsMap =
      ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.sampleTimeTaskIDArray;
    mdlTsMap[0] = 0;
    ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.sampleTimeTaskIDPtr =
      (&mdlTsMap[0]);
    ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.sampleTimes =
      (&ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.sampleTimesArray[0]);
    ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.offsetTimes =
      (&ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.offsetTimesArray[0]);

    /* task periods */
    ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.sampleTimes[0] = (0.005);

    /* task offsets */
    ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.offsetTimes[0] = (0.0);
  }

  rtmSetTPtr(ClosedLoopSystem_PID_Exp_python_block_2_M,
             &ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.tArray[0]);

  {
    int_T *mdlSampleHits =
      ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.sampleHitArray;
    mdlSampleHits[0] = 1;
    ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.sampleHits =
      (&mdlSampleHits[0]);
  }

  rtmSetTFinal(ClosedLoopSystem_PID_Exp_python_block_2_M, 100.0);
  ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.stepSize0 = 0.005;

  /* External mode info */
  ClosedLoopSystem_PID_Exp_python_block_2_M->Sizes.checksums[0] = (879925908U);
  ClosedLoopSystem_PID_Exp_python_block_2_M->Sizes.checksums[1] = (680770245U);
  ClosedLoopSystem_PID_Exp_python_block_2_M->Sizes.checksums[2] = (2722360832U);
  ClosedLoopSystem_PID_Exp_python_block_2_M->Sizes.checksums[3] = (1046960713U);

  {
    static const sysRanDType rtAlwaysEnabled = SUBSYS_RAN_BC_ENABLE;
    static RTWExtModeInfo rt_ExtModeInfo;
    static const sysRanDType *systemRan[2];
    ClosedLoopSystem_PID_Exp_python_block_2_M->extModeInfo = (&rt_ExtModeInfo);
    rteiSetSubSystemActiveVectorAddresses(&rt_ExtModeInfo, systemRan);
    systemRan[0] = &rtAlwaysEnabled;
    systemRan[1] = (sysRanDType *)
      &ClosedLoopSystem_PID_Exp_python_block_2_DW.RealTimeSync_SubsysRanBC;
    rteiSetModelMappingInfoPtr
      (ClosedLoopSystem_PID_Exp_python_block_2_M->extModeInfo,
       &ClosedLoopSystem_PID_Exp_python_block_2_M->SpecialInfo.mappingInfo);
    rteiSetChecksumsPtr(ClosedLoopSystem_PID_Exp_python_block_2_M->extModeInfo,
                        ClosedLoopSystem_PID_Exp_python_block_2_M->Sizes.checksums);
    rteiSetTPtr(ClosedLoopSystem_PID_Exp_python_block_2_M->extModeInfo,
                rtmGetTPtr(ClosedLoopSystem_PID_Exp_python_block_2_M));
  }

  ClosedLoopSystem_PID_Exp_python_block_2_M->solverInfoPtr =
    (&ClosedLoopSystem_PID_Exp_python_block_2_M->solverInfo);
  ClosedLoopSystem_PID_Exp_python_block_2_M->Timing.stepSize = (0.005);
  rtsiSetFixedStepSize(&ClosedLoopSystem_PID_Exp_python_block_2_M->solverInfo,
                       0.005);
  rtsiSetSolverMode(&ClosedLoopSystem_PID_Exp_python_block_2_M->solverInfo,
                    SOLVER_MODE_SINGLETASKING);

  /* block I/O */
  ClosedLoopSystem_PID_Exp_python_block_2_M->blockIO = ((void *)
    &ClosedLoopSystem_PID_Exp_python_block_2_B);
  (void) memset(((void *) &ClosedLoopSystem_PID_Exp_python_block_2_B), 0,
                sizeof(B_ClosedLoopSystem_PID_Exp_python_block_2_T));

  /* parameters */
  ClosedLoopSystem_PID_Exp_python_block_2_M->defaultParam = ((real_T *)
    &ClosedLoopSystem_PID_Exp_python_block_2_P);

  /* states (dwork) */
  ClosedLoopSystem_PID_Exp_python_block_2_M->dwork = ((void *)
    &ClosedLoopSystem_PID_Exp_python_block_2_DW);
  (void) memset((void *)&ClosedLoopSystem_PID_Exp_python_block_2_DW, 0,
                sizeof(DW_ClosedLoopSystem_PID_Exp_python_block_2_T));

  /* data type transition information */
  {
    static DataTypeTransInfo dtInfo;
    (void) memset((char_T *) &dtInfo, 0,
                  sizeof(dtInfo));
    ClosedLoopSystem_PID_Exp_python_block_2_M->SpecialInfo.mappingInfo =
      (&dtInfo);
    dtInfo.numDataTypes = 23;
    dtInfo.dataTypeSizes = &rtDataTypeSizes[0];
    dtInfo.dataTypeNames = &rtDataTypeNames[0];

    /* Block I/O transition table */
    dtInfo.BTransTable = &rtBTransTable;

    /* Parameters transition table */
    dtInfo.PTransTable = &rtPTransTable;
  }

  /* Initialize Sizes */
  ClosedLoopSystem_PID_Exp_python_block_2_M->Sizes.numContStates = (0);/* Number of continuous states */
  ClosedLoopSystem_PID_Exp_python_block_2_M->Sizes.numY = (0);/* Number of model outputs */
  ClosedLoopSystem_PID_Exp_python_block_2_M->Sizes.numU = (0);/* Number of model inputs */
  ClosedLoopSystem_PID_Exp_python_block_2_M->Sizes.sysDirFeedThru = (0);/* The model is not direct feedthrough */
  ClosedLoopSystem_PID_Exp_python_block_2_M->Sizes.numSampTimes = (1);/* Number of sample times */
  ClosedLoopSystem_PID_Exp_python_block_2_M->Sizes.numBlocks = (12);/* Number of blocks */
  ClosedLoopSystem_PID_Exp_python_block_2_M->Sizes.numBlockIO = (9);/* Number of block outputs */
  ClosedLoopSystem_PID_Exp_python_block_2_M->Sizes.numBlockPrms = (9);/* Sum of parameter "widths" */
  return ClosedLoopSystem_PID_Exp_python_block_2_M;
}

/*========================================================================*
 * End of Classic call interface                                          *
 *========================================================================*/
