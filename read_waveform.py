#!/usr/bin/env python

import sys
import re
import numpy as np
import h5py
import argparse

def main():

    #maxEvents = 10000
    #for arg in sys.argv[1:]:
    #    if isinstance(arg, str):
    #        print("Reading File " + arg)
    #        filename = arg
    #    if isinstance(arg, int):
    #        print("Number of events " + arg)
    #        maxEvents = arg

    parser = argparse.ArgumentParser(description = 'Converte saida do Wavedump para hdf5')
    parser.add_argument('fileName', help = 'Arquivo de entrada' )
    parser.add_argument('-n', '--events', dest = 'events', type = int, required = False, default = 10000, help = 'Numero de eventos' )
    #parser.add_argument('-f', action = 'store', dest = 'txt', required = True, help = 'Saida do Wavedump' )
    parser.add_argument('-v', '--verbose', action = 'store_true', dest = 'debug', required = False, help = 'Flag de debug' )
    args = parser.parse_args()

    fileName = args.fileName
    events = args.events
    print( "Number of events {:d}".format( events ) )
    print( "Reading File " + fileName )

    dsetMax = 1000
    file_str = ( fileName.split('/')[-1] ).split('.')[0]
    with h5py.File('output-' + file_str + '.h5', 'w') as f:

        # 1024 length waveform
        dset = f.create_dataset('Waveform', (dsetMax,1024), compression="gzip", chunks=True, maxshape=(None,1024))
        # Event number, Channel
        dset_metadata = f.create_dataset('Metadata', (dsetMax,2), compression="gzip", chunks=True, maxshape=(None,2))
        
        waveforms = open(fileName, "r")
        record_length = -1
        board_id = -1
        channel = -1
        event_number = -1
        pattern = -1
        trigger = -1
        offset = -1
        index_cell = -1
        arr = []
        p_record_length = re.compile('Record Length: *')
        p_board_id = re.compile('Board ID: *')
        p_channel = re.compile('Channel: *')
        p_event_number = re.compile('Event Number: *')
        p_pattern = re.compile('Pattern: *')
        p_trigger = re.compile('Trigger Time Stamp: *')
        p_offset = re.compile("DC offset \\(DAC\\): *")
        p_index_cell = re.compile('Start Index Cell: *')

        #data = []
        dset_slice = 0
        dset_idx = 0
        n_events_recorded = 0
        print ( dset.shape )
        for idx, line in enumerate(waveforms):
            #if events >= 0 and len(data) >= events: break
            if events >= 0 and n_events_recorded >= events: break

            m_record_length = p_record_length.match( line )
            m_board_id = p_board_id.match( line )
            m_channel = p_channel.match( line )
            m_event_number = p_event_number.match( line )
            m_pattern = p_pattern.match( line )
            m_trigger = p_trigger.match( line )
            m_offset = p_offset.match( line )
            m_index_cell = p_index_cell.match( line )

            if m_record_length:
                record_length = int( line[m_record_length.end():] )
                print (line, record_length)
                start_array = False
                arr_entry = -1
            elif m_board_id:
                board_id = int(line[m_board_id.end():])
                print(line, board_id)
            elif m_channel:
                channel = int(line[m_channel.end():])
                print(line, channel)
            elif m_event_number:
                event_number = int( line[m_event_number.end():] )
                print (line, event_number)
            elif m_pattern:
                pattern = int(line[m_pattern.end():], 0)
                print(line, pattern)
            elif m_trigger:
                trigger = int(line[m_trigger.end():])
                print(line, trigger)
            elif m_offset:
                offset = int( line[m_offset.end():], 0)
                print (line, offset)
            elif m_index_cell:
                index_cell = int(line[m_index_cell.end():])
                print(line, index_cell)
                start_array = True
            else:
                if start_array:
                    if arr_entry == -1:
                        #arr.append(np.zeros( record_length ))
                        arr = np.zeros( record_length )
                        arr_entry = 0

                    val = float( line.rstrip() )
                    #arr[channel][arr_entry] = val
                    arr[arr_entry] = val
                    arr_entry += 1
                    #if arr_entry == (record_length) and channel > 0:
                    if arr_entry == (record_length):
                        print (arr)
                        #data.append(arr)
                        if dset_idx == dsetMax:
                            dset_slice += 1
                            dset_idx = 0
                            dset.resize( ( dset.shape[0] + dsetMax ), axis=0 )
                            dset_metadata.resize( ( dset.shape[0] + dsetMax ), axis=0 )
                            print ( dset.shape )
                            print ( dset_metadata.shape )

                        dset[ ( dset_slice*dsetMax + dset_idx ) ] = arr
                        dset_metadata[ ( dset_slice*dsetMax + dset_idx ) ] = (event_number,channel)
                        dset_idx += 1
                        n_events_recorded += 1
                        print ( "Number of events recorded: {:d}".format( n_events_recorded ) )

                        arr = None

        #dset = f.create_dataset('Vals', data=data)
        dset.resize( n_events_recorded, axis=0 )
        dset_metadata.resize( n_events_recorded, axis=0 )

        print ( dset.shape )
        print ( dset_metadata.shape )
        print ( dset[-1] )
        print ( dset_metadata[-1] )
        print ( "Number of events recorded: {:d}".format( n_events_recorded ) )

if __name__== '__main__':
    main()
