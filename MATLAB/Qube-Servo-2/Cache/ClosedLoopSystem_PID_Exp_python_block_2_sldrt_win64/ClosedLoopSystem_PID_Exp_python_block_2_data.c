/*
 * ClosedLoopSystem_PID_Exp_python_block_2_data.c
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

/* Block parameters (default storage) */
P_ClosedLoopSystem_PID_Exp_python_block_2_T
  ClosedLoopSystem_PID_Exp_python_block_2_P = {
  /* Mask Parameter: RealTimeSynchronization_MaxMissedTicks
   * Referenced by: '<S4>/Real-Time Synchronization'
   */
  0.0,

  /* Mask Parameter: RealTimeSynchronization_MaxMissedTicks_f
   * Referenced by: '<Root>/Real-Time Synchronization'
   */
  100.0,

  /* Mask Parameter: RealTimeSynchronization_YieldWhenWaiting
   * Referenced by: '<S4>/Real-Time Synchronization'
   */
  0.0,

  /* Mask Parameter: RealTimeSynchronization_YieldWhenWaiting_g
   * Referenced by: '<Root>/Real-Time Synchronization'
   */
  0.0,

  /* Expression: 0
   * Referenced by: '<Root>/Constant5'
   */
  0.0,

  /* Expression: 180/pi
   * Referenced by: '<S2>/Gain'
   */
  57.295779513082323,

  /* Expression: 180/pi
   * Referenced by: '<S3>/Gain'
   */
  57.295779513082323,

  /* Expression: 1
   * Referenced by: '<S1>/Synchronization'
   */
  1.0,

  /* Computed Parameter: Constant6_Value
   * Referenced by: '<Root>/Constant6'
   */
  true
};
