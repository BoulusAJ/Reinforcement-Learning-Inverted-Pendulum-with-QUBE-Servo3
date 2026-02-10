    function targMap = targDataMap(),

    ;%***********************
    ;% Create Parameter Map *
    ;%***********************
    
        nTotData      = 0; %add to this count as we go
        nTotSects     = 2;
        sectIdxOffset = 0;

        ;%
        ;% Define dummy sections & preallocate arrays
        ;%
        dumSection.nData = -1;
        dumSection.data  = [];

        dumData.logicalSrcIdx = -1;
        dumData.dtTransOffset = -1;

        ;%
        ;% Init/prealloc paramMap
        ;%
        paramMap.nSections           = nTotSects;
        paramMap.sectIdxOffset       = sectIdxOffset;
            paramMap.sections(nTotSects) = dumSection; %prealloc
        paramMap.nTotData            = -1;

        ;%
        ;% Auto data (ClosedLoopSystem_PID_Exp_python_block_2_P)
        ;%
            section.nData     = 8;
            section.data(8)  = dumData; %prealloc

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_P.RealTimeSynchronization_MaxMissedTicks
                    section.data(1).logicalSrcIdx = 0;
                    section.data(1).dtTransOffset = 0;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_P.RealTimeSynchronization_MaxMissedTicks_f
                    section.data(2).logicalSrcIdx = 1;
                    section.data(2).dtTransOffset = 1;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_P.RealTimeSynchronization_YieldWhenWaiting
                    section.data(3).logicalSrcIdx = 2;
                    section.data(3).dtTransOffset = 2;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_P.RealTimeSynchronization_YieldWhenWaiting_g
                    section.data(4).logicalSrcIdx = 3;
                    section.data(4).dtTransOffset = 3;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_P.Constant5_Value
                    section.data(5).logicalSrcIdx = 4;
                    section.data(5).dtTransOffset = 4;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_P.Gain_Gain
                    section.data(6).logicalSrcIdx = 5;
                    section.data(6).dtTransOffset = 5;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_P.Gain_Gain_n
                    section.data(7).logicalSrcIdx = 6;
                    section.data(7).dtTransOffset = 6;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_P.Synchronization_Value
                    section.data(8).logicalSrcIdx = 7;
                    section.data(8).dtTransOffset = 7;

            nTotData = nTotData + section.nData;
            paramMap.sections(1) = section;
            clear section

            section.nData     = 1;
            section.data(1)  = dumData; %prealloc

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_P.Constant6_Value
                    section.data(1).logicalSrcIdx = 8;
                    section.data(1).dtTransOffset = 0;

            nTotData = nTotData + section.nData;
            paramMap.sections(2) = section;
            clear section


            ;%
            ;% Non-auto Data (parameter)
            ;%


        ;%
        ;% Add final counts to struct.
        ;%
        paramMap.nTotData = nTotData;



    ;%**************************
    ;% Create Block Output Map *
    ;%**************************
    
        nTotData      = 0; %add to this count as we go
        nTotSects     = 2;
        sectIdxOffset = 0;

        ;%
        ;% Define dummy sections & preallocate arrays
        ;%
        dumSection.nData = -1;
        dumSection.data  = [];

        dumData.logicalSrcIdx = -1;
        dumData.dtTransOffset = -1;

        ;%
        ;% Init/prealloc sigMap
        ;%
        sigMap.nSections           = nTotSects;
        sigMap.sectIdxOffset       = sectIdxOffset;
            sigMap.sections(nTotSects) = dumSection; %prealloc
        sigMap.nTotData            = -1;

        ;%
        ;% Auto data (ClosedLoopSystem_PID_Exp_python_block_2_B)
        ;%
            section.nData     = 8;
            section.data(8)  = dumData; %prealloc

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o1
                    section.data(1).logicalSrcIdx = 0;
                    section.data(1).dtTransOffset = 0;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o2
                    section.data(2).logicalSrcIdx = 1;
                    section.data(2).dtTransOffset = 1;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o3
                    section.data(3).logicalSrcIdx = 2;
                    section.data(3).dtTransOffset = 2;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o4
                    section.data(4).logicalSrcIdx = 3;
                    section.data(4).dtTransOffset = 3;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o5
                    section.data(5).logicalSrcIdx = 4;
                    section.data(5).dtTransOffset = 4;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_B.PythonCode1_o6
                    section.data(6).logicalSrcIdx = 5;
                    section.data(6).dtTransOffset = 5;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_B.Gain
                    section.data(7).logicalSrcIdx = 6;
                    section.data(7).dtTransOffset = 6;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_B.Gain_h
                    section.data(8).logicalSrcIdx = 7;
                    section.data(8).dtTransOffset = 7;

            nTotData = nTotData + section.nData;
            sigMap.sections(1) = section;
            clear section

            section.nData     = 1;
            section.data(1)  = dumData; %prealloc

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_B.RealTimeSynchronization
                    section.data(1).logicalSrcIdx = 8;
                    section.data(1).dtTransOffset = 0;

            nTotData = nTotData + section.nData;
            sigMap.sections(2) = section;
            clear section


            ;%
            ;% Non-auto Data (signal)
            ;%


        ;%
        ;% Add final counts to struct.
        ;%
        sigMap.nTotData = nTotData;



    ;%*******************
    ;% Create DWork Map *
    ;%*******************
    
        nTotData      = 0; %add to this count as we go
        nTotSects     = 2;
        sectIdxOffset = 2;

        ;%
        ;% Define dummy sections & preallocate arrays
        ;%
        dumSection.nData = -1;
        dumSection.data  = [];

        dumData.logicalSrcIdx = -1;
        dumData.dtTransOffset = -1;

        ;%
        ;% Init/prealloc dworkMap
        ;%
        dworkMap.nSections           = nTotSects;
        dworkMap.sectIdxOffset       = sectIdxOffset;
            dworkMap.sections(nTotSects) = dumSection; %prealloc
        dworkMap.nTotData            = -1;

        ;%
        ;% Auto data (ClosedLoopSystem_PID_Exp_python_block_2_DW)
        ;%
            section.nData     = 5;
            section.data(5)  = dumData; %prealloc

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_DW.Scope2_PWORK.LoggedData
                    section.data(1).logicalSrcIdx = 0;
                    section.data(1).dtTransOffset = 0;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_DW.TAQSigLogging_InsertedFor_PythonCode1_at_outport_0_PWORK.AQHandles
                    section.data(2).logicalSrcIdx = 1;
                    section.data(2).dtTransOffset = 3;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_DW.RealTimeSynchronization_PWORK
                    section.data(3).logicalSrcIdx = 2;
                    section.data(3).dtTransOffset = 4;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_DW.Scope3_PWORK.LoggedData
                    section.data(4).logicalSrcIdx = 3;
                    section.data(4).dtTransOffset = 5;

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_DW.RealTimeSynchronization_PWORK_h
                    section.data(5).logicalSrcIdx = 4;
                    section.data(5).dtTransOffset = 6;

            nTotData = nTotData + section.nData;
            dworkMap.sections(1) = section;
            clear section

            section.nData     = 1;
            section.data(1)  = dumData; %prealloc

                    ;% ClosedLoopSystem_PID_Exp_python_block_2_DW.RealTimeSync_SubsysRanBC
                    section.data(1).logicalSrcIdx = 5;
                    section.data(1).dtTransOffset = 0;

            nTotData = nTotData + section.nData;
            dworkMap.sections(2) = section;
            clear section


            ;%
            ;% Non-auto Data (dwork)
            ;%


        ;%
        ;% Add final counts to struct.
        ;%
        dworkMap.nTotData = nTotData;



    ;%
    ;% Add individual maps to base struct.
    ;%

    targMap.paramMap  = paramMap;
    targMap.signalMap = sigMap;
    targMap.dworkMap  = dworkMap;

    ;%
    ;% Add checksums to base struct.
    ;%


    targMap.checksum0 = 879925908;
    targMap.checksum1 = 680770245;
    targMap.checksum2 = 2722360832;
    targMap.checksum3 = 1046960713;

