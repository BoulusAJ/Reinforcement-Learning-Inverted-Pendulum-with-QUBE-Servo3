/*
 * rotary_pendulum_sldrt.c
 *
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * Code generation for model "rotary_pendulum_sldrt".
 *
 * Model version              : 1.146
 * Simulink Coder version : 25.2 (R2025b) 28-Jul-2025
 * C source code generated on : Tue Feb 10 10:57:19 2026
 *
 * Target selection: sldrt.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Intel->x86-64 (Linux 64)
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "rotary_pendulum_sldrt.h"
#include <string.h>
#include "rotary_pendulum_sldrt_dt.h"

/* list of Simulink Desktop Real-Time timers */
const int SLDRTTimerCount = 1;
const double SLDRTTimers[2] = {
  5.0E-5, 0.0,
};

/* Block states (default storage) */
DW_rotary_pendulum_sldrt_T rotary_pendulum_sldrt_DW;

/* Real-time model */
static RT_MODEL_rotary_pendulum_sldrt_T rotary_pendulum_sldrt_M_;
RT_MODEL_rotary_pendulum_sldrt_T *const rotary_pendulum_sldrt_M =
  &rotary_pendulum_sldrt_M_;

/* Model output function */
void rotary_pendulum_sldrt_output(void)
{
  /* Reset subsysRan breadcrumbs */
  srClearBC(rotary_pendulum_sldrt_DW.RealTimeSync_SubsysRanBC);

  /* Outputs for Enabled SubSystem: '<S1>/Real-Time Sync' incorporates:
   *  EnablePort: '<S2>/Enable'
   */
  /* Constant: '<S1>/Synchronization' */
  if (rotary_pendulum_sldrt_P.Synchronization_Value > 0.0) {
    /* S-Function (sldrtsync): '<S2>/Real-Time Synchronization' */
    /* S-Function Block: <S2>/Real-Time Synchronization */
    {
    }

    srUpdateBC(rotary_pendulum_sldrt_DW.RealTimeSync_SubsysRanBC);
  }

  /* End of Constant: '<S1>/Synchronization' */
  /* End of Outputs for SubSystem: '<S1>/Real-Time Sync' */
}

/* Model update function */
void rotary_pendulum_sldrt_update(void)
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
  if (!(++rotary_pendulum_sldrt_M->Timing.clockTick0)) {
    ++rotary_pendulum_sldrt_M->Timing.clockTickH0;
  }

  rotary_pendulum_sldrt_M->Timing.t[0] =
    rotary_pendulum_sldrt_M->Timing.clockTick0 *
    rotary_pendulum_sldrt_M->Timing.stepSize0 +
    rotary_pendulum_sldrt_M->Timing.clockTickH0 *
    rotary_pendulum_sldrt_M->Timing.stepSize0 * 4294967296.0;
}

/* Model initialize function */
void rotary_pendulum_sldrt_initialize(void)
{
}

/* Model terminate function */
void rotary_pendulum_sldrt_terminate(void)
{
  /* (no terminate code required) */
}

/*========================================================================*
 * Start of Classic call interface                                        *
 *========================================================================*/
void MdlOutputs(int_T tid)
{
  rotary_pendulum_sldrt_output();
  UNUSED_PARAMETER(tid);
}

void MdlUpdate(int_T tid)
{
  rotary_pendulum_sldrt_update();
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
  rotary_pendulum_sldrt_initialize();
}

void MdlTerminate(void)
{
  rotary_pendulum_sldrt_terminate();
}

/* Registration function */
RT_MODEL_rotary_pendulum_sldrt_T *rotary_pendulum_sldrt(void)
{
  /* Registration code */

  /* initialize real-time model */
  (void) memset((void *)rotary_pendulum_sldrt_M, 0,
                sizeof(RT_MODEL_rotary_pendulum_sldrt_T));

  /* Initialize timing info */
  {
    int_T *mdlTsMap = rotary_pendulum_sldrt_M->Timing.sampleTimeTaskIDArray;
    mdlTsMap[0] = 0;
    rotary_pendulum_sldrt_M->Timing.sampleTimeTaskIDPtr = (&mdlTsMap[0]);
    rotary_pendulum_sldrt_M->Timing.sampleTimes =
      (&rotary_pendulum_sldrt_M->Timing.sampleTimesArray[0]);
    rotary_pendulum_sldrt_M->Timing.offsetTimes =
      (&rotary_pendulum_sldrt_M->Timing.offsetTimesArray[0]);

    /* task periods */
    rotary_pendulum_sldrt_M->Timing.sampleTimes[0] = (5.0E-5);

    /* task offsets */
    rotary_pendulum_sldrt_M->Timing.offsetTimes[0] = (0.0);
  }

  rtmSetTPtr(rotary_pendulum_sldrt_M, &rotary_pendulum_sldrt_M->Timing.tArray[0]);

  {
    int_T *mdlSampleHits = rotary_pendulum_sldrt_M->Timing.sampleHitArray;
    mdlSampleHits[0] = 1;
    rotary_pendulum_sldrt_M->Timing.sampleHits = (&mdlSampleHits[0]);
  }

  rtmSetTFinal(rotary_pendulum_sldrt_M, -1);
  rotary_pendulum_sldrt_M->Timing.stepSize0 = 5.0E-5;

  /* External mode info */
  rotary_pendulum_sldrt_M->Sizes.checksums[0] = (3782384060U);
  rotary_pendulum_sldrt_M->Sizes.checksums[1] = (1255972385U);
  rotary_pendulum_sldrt_M->Sizes.checksums[2] = (2404980127U);
  rotary_pendulum_sldrt_M->Sizes.checksums[3] = (1072561843U);

  {
    static const sysRanDType rtAlwaysEnabled = SUBSYS_RAN_BC_ENABLE;
    static RTWExtModeInfo rt_ExtModeInfo;
    static const sysRanDType *systemRan[2];
    rotary_pendulum_sldrt_M->extModeInfo = (&rt_ExtModeInfo);
    rteiSetSubSystemActiveVectorAddresses(&rt_ExtModeInfo, systemRan);
    systemRan[0] = &rtAlwaysEnabled;
    systemRan[1] = (sysRanDType *)
      &rotary_pendulum_sldrt_DW.RealTimeSync_SubsysRanBC;
    rteiSetModelMappingInfoPtr(rotary_pendulum_sldrt_M->extModeInfo,
      &rotary_pendulum_sldrt_M->SpecialInfo.mappingInfo);
    rteiSetChecksumsPtr(rotary_pendulum_sldrt_M->extModeInfo,
                        rotary_pendulum_sldrt_M->Sizes.checksums);
    rteiSetTPtr(rotary_pendulum_sldrt_M->extModeInfo, rtmGetTPtr
                (rotary_pendulum_sldrt_M));
  }

  rotary_pendulum_sldrt_M->solverInfoPtr = (&rotary_pendulum_sldrt_M->solverInfo);
  rotary_pendulum_sldrt_M->Timing.stepSize = (5.0E-5);
  rtsiSetFixedStepSize(&rotary_pendulum_sldrt_M->solverInfo, 5.0E-5);
  rtsiSetSolverMode(&rotary_pendulum_sldrt_M->solverInfo,
                    SOLVER_MODE_SINGLETASKING);

  /* parameters */
  rotary_pendulum_sldrt_M->defaultParam = ((real_T *)&rotary_pendulum_sldrt_P);

  /* states (dwork) */
  rotary_pendulum_sldrt_M->dwork = ((void *) &rotary_pendulum_sldrt_DW);
  (void) memset((void *)&rotary_pendulum_sldrt_DW, 0,
                sizeof(DW_rotary_pendulum_sldrt_T));

  /* data type transition information */
  {
    static DataTypeTransInfo dtInfo;
    (void) memset((char_T *) &dtInfo, 0,
                  sizeof(dtInfo));
    rotary_pendulum_sldrt_M->SpecialInfo.mappingInfo = (&dtInfo);
    dtInfo.numDataTypes = 23;
    dtInfo.dataTypeSizes = &rtDataTypeSizes[0];
    dtInfo.dataTypeNames = &rtDataTypeNames[0];

    /* Block I/O transition table */
    dtInfo.BTransTable = &rtBTransTable;

    /* Parameters transition table */
    dtInfo.PTransTable = &rtPTransTable;
  }

  /* Initialize Sizes */
  rotary_pendulum_sldrt_M->Sizes.numContStates = (0);/* Number of continuous states */
  rotary_pendulum_sldrt_M->Sizes.numY = (0);/* Number of model outputs */
  rotary_pendulum_sldrt_M->Sizes.numU = (0);/* Number of model inputs */
  rotary_pendulum_sldrt_M->Sizes.sysDirFeedThru = (0);/* The model is not direct feedthrough */
  rotary_pendulum_sldrt_M->Sizes.numSampTimes = (1);/* Number of sample times */
  rotary_pendulum_sldrt_M->Sizes.numBlocks = (3);/* Number of blocks */
  rotary_pendulum_sldrt_M->Sizes.numBlockIO = (0);/* Number of block outputs */
  rotary_pendulum_sldrt_M->Sizes.numBlockPrms = (3);/* Sum of parameter "widths" */
  return rotary_pendulum_sldrt_M;
}

/*========================================================================*
 * End of Classic call interface                                          *
 *========================================================================*/
