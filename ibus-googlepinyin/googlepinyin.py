#!/usr/bin/python
# -*- coding: UTF-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
'''libgooglepinyin wrapper for python

'''

import ctypes
import ctypes.util
import os
import sys

libc = ctypes.CDLL("libc.so.6")
ime_pinyin = ctypes.CDLL(ctypes.util.find_library('googlepinyin'), use_errno=True)

_a = lambda path: os.path.exists(path) and path or ""
FN_SYS_DICT = _a('/usr/share/googlepinyin/dict_pinyin.dat')\
           or _a('/usr/local/share/googlepinyin/dict_pinyin.dat')
FN_USR_DICT = os.path.expanduser('~/.config/ibus/googlepinyin/userdict_pinyin.dat')

kMaxLemmaSize = 8
kMaxPredictSize = kMaxLemmaSize - 1

def im_open_decoder(fn_sys_dict=FN_SYS_DICT, fn_usr_dict=FN_USR_DICT):
    '''Open the decoder engine

    c-def
    =====
    /**
     * Open the decoder engine via the system and user dictionary file names.
     *
     * @param fn_sys_dict The file name of the system dictionary.
     * @param fn_usr_dict The file name of the user dictionary.
     * @return true if open the decoder engine successfully.
     */
    bool im_open_decoder(const char *fn_sys_dict, const char *fn_usr_dict);
    '''
    if not os.path.exists(os.path.dirname(fn_usr_dict)):
        os.makedirs(os.path.dirname(fn_usr_dict))
        pass
    return ime_pinyin.im_open_decoder(fn_sys_dict, fn_usr_dict)

def im_close_decoder():
    '''Close the decoder engine

    c-def
    =====
    /**
     * Close the decoder engine.
     */
    void im_close_decoder();
    '''
    ime_pinyin.im_close_decoder()
    pass

def im_set_max_lens(max_sps_len, max_hzs_len):
    '''Set maximum limitations for decoding

    c-def
    =====
    /**
     * Set maximum limitations for decoding. If this function is not called,
     * default values will be used. For example, due to screen size limitation,
     * the UI engine of the IME can only show a certain number of letters(input)
     * to decode, and a certain number of Chinese characters(output). If after
     * user adds a new letter, the input or the output string is longer than the
     * limitations, the engine will discard the recent letter.
     *
     * @param max_sps_len Maximum length of the spelling string(Pinyin string).
     * @max_hzs_len Maximum length of the decoded Chinese character string.
     */
    void im_set_max_lens(size_t max_sps_len, size_t max_hzs_len);
    '''
    ime_pinyin.im_set_max_lens(max_sps_len, max_hzs_len)
    pass

def im_flush_cache():
    '''Flush cached data to persistent memory

    c-def
    =====
    /**
     * Flush cached data to persistent memory. Because at runtime, in order to
     * achieve best performance, some data is only store in memory.
     */
    void im_flush_cache();
    '''
    return ime_pinyin.im_flush_cache()

def im_search(pinyin_string):
    '''Use a spelling string(Pinyin string) to search

    c-def
    =====
    /**
     * Use a spelling string(Pinyin string) to search. The engine will try to do
     * an incremental search based on its previous search result, so if the new
     * string has the same prefix with the previous one stored in the decoder,
     * the decoder will only continue the search from the end of the prefix.
     * If the caller needs to do a brand new search, please call im_reset_search()
     * first. Calling im_search() is equivalent to calling im_add_letter() one by
     * one.
     *
     * @param sps_buf The spelling string buffer to decode.
     * @param sps_len The length of the spelling string buffer.
     * @return The number of candidates.
     */
    size_t im_search(const char* sps_buf, size_t sps_len);
    '''
    candidates_num = ime_pinyin.im_search(pinyin_string, len(pinyin_string))
    return candidates_num

def im_delsearch(pos, is_pos_in_splid, clear_fixed_this_step):
    '''Make a delete operation in the current search result, and make research if necessary

    c-def
    =====
    /**
     * Make a delete operation in the current search result, and make research if
     * necessary.
     *
     * @param pos The posistion of char in spelling string to delete, or the
     * position of spelling id in result string to delete.
     * @param is_pos_in_splid Indicate whether the pos parameter is the position
     * in the spelling string, or the position in the result spelling id string.
     * @return The number of candidates.
     */
    size_t im_delsearch(size_t pos, bool is_pos_in_splid,
                      bool clear_fixed_this_step);
    '''
    return ime_pinyin.im_delsearch(pos, is_pos_in_splid, clear_fixed_this_step)

def im_reset_search():
    '''Reset the previous search result

    c-def
    =====
    /**
     * Reset the previous search result.
     */
    void im_reset_search();
    '''
    ime_pinyin.im_reset_search()
    pass

def im_get_sps_str(decoded_len):
    '''Get the spelling string kept by the decoder

    c-def
    =====
    /**
     * Get the spelling string kept by the decoder.
     *
     * @param decoded_len Used to return how many characters in the spelling
     * string is successfully parsed.
     * @return The spelling string kept by the decoder.
     */
    const char *im_get_sps_str(size_t *decoded_len);
    '''
    return ime_pinyin.im_get_sps_str(decoded_len)


def im_get_candidate(cand_id, max_len=1024):
    '''Get a candidate(or choice) string.

    c-def
    =====
    /**
     * Get a candidate(or choice) string.
     *
     * @param cand_id The id to get a candidate. Started from 0. Usually, id 0
     * is a sentence-level candidate.
     * @param cand_str The buffer to store the candidate.
     * @param max_len The maximum length of the buffer.
     * @return cand_str if succeeds, otherwise NULL.
     */
    char16* im_get_candidate(size_t cand_id, char16* cand_str,
                             size_t max_len);
    '''
    cand_str = ctypes.c_buffer(256)
    candidate = ime_pinyin.im_get_candidate(cand_id, cand_str, max_len)
    # ret = ctypes.c_char_p(candidate).value.decode('utf16').encode('utf8')
    return cand_str.raw.decode('utf16').encode('utf8').replace('\x00', '')

_spl_start = ctypes.c_uint16()

def im_get_spl_start_pos():
    '''Get the segmentation information(the starting positions) of the spelling string

    c-def
    =====
    /**
     * Get the segmentation information(the starting positions) of the spelling
     * string.
     *
     * @param spl_start Used to return the starting posistions.
     * @return The number of spelling ids. If it is L, there will be L+1 valid
     * elements in spl_start, and spl_start[L] is the posistion after the end of
     * the last spelling id.
     */
    size_t im_get_spl_start_pos(const uint16 *&spl_start);
    '''
    num = ime_pinyin.im_get_spl_start_pos(_spl_start)
    return _spl_start.value
    
_cand_id = ctypes.c_size_t()

def im_choose(cand_id):
    '''Choose a candidate and make it fixed

    c-def
    =====
    /**
     * Choose a candidate and make it fixed. If the candidate does not match
     * the end of all spelling ids, new candidates will be provided from the
     * first unfixed position. If the candidate matches the end of the all
     * spelling ids, there will be only one new candidates, or the whole fixed
     * sentence.
     *
     * @param cand_id The id of candidate to select and make it fixed.
     * @return The number of candidates. If after the selection, the whole result
     * string has been fixed, there will be only one candidate.
     */
    size_t im_choose(size_t cand_id);
    '''
    _cand_id.value = cand_id
    return ime_pinyin.im_choose(_cand_id)

def im_cancel_last_choice():
    '''Cancel the last selection

    c-def
    =====
    /**
     * Cancel the last selection, or revert the last operation of im_choose().
     *
     * @return The number of candidates.
     */
    size_t im_cancel_last_choice();
    '''
    return ime_pinyin.im_cancel_last_choice()

def im_get_fixed_len():
    '''Get the number of fixed spelling ids, or Chinese characters

    c-def
    =====
    /**
     * Get the number of fixed spelling ids, or Chinese characters.
     *
     * @return The number of fixed spelling ids, of Chinese characters.
     */
    size_t im_get_fixed_len();
    '''
    return ime_pinyin.im_get_fixed_len()

_pre_buf = ctypes.c_buffer((kMaxPredictSize + 1)*2 + 2)

def im_get_predicts(his_buf):
    '''Get prediction candiates based on the given fixed Chinese string as the history

    c-def
    =====
    /**
     * Get prediction candiates based on the given fixed Chinese string as the
     * history.
     *
     * @param his_buf The history buffer to do the prediction. It should be ended
     * with '\0'.
     * @param pre_buf Used to return prediction result list.
     * @return The number of predicted result string.
     */
    size_t im_get_predicts(const char16 *his_buf,
                           char16 (*&pre_buf)[kMaxPredictSize + 1]);
    '''
    his_buf = his_buf.decode('utf8').encode('utf16') + '\0'
    num = ime_pinyin.im_get_predicts(his_buf, _pre_buf)
    return _pre_buf.value.decode('utf16').encode('utf8')

def im_enable_shm_as_szm(enable):
    '''Enable Shengmus in ShouZiMu mode

    c-def
    =====
    /**
     * Enable Shengmus in ShouZiMu mode.
     */
    void im_enable_shm_as_szm(bool enable);
    '''
    return ime_pinyin.im_enable_shm_as_szm(enable)

def im_enable_ym_as_szm(enable):
    '''Enable Yunmus in ShouZiMu mode

    c-def
    =====
    /**
     * Enable Yunmus in ShouZiMu mode.
     */
    void im_enable_ym_as_szm(bool enable);
    '''
    return ime_pinyin.im_enable_ym_as_szm(engine)

if __name__=="__main__":
    if sys.argv[1:] and sys.argv[1].isalpha():
        pinyin = sys.argv[1]
        im_open_decoder()
        num = im_search(pinyin)
        print '\t'.join((('%3s %s') % (i, im_get_candidate(i)) for i in range(num)))
        pass
    else:
        try:
            import readline
        except:
            pass
        im_open_decoder()
        num = 0
        while True:
            try:
                i = raw_input('> ')
            except:
                im_close_decoder()
                break
            if i and i[0].isalpha():
                im_reset_search()
                num = im_search(i)
                print '\t'.join((('%3s %s') % (i, im_get_candidate(i)) for i in range(num)))
                pass
            elif i.isdigit() and int(i) < num:
                num = im_choose(int(i))
                print '-', im_get_fixed_len()
                print '\t'.join((('%3s %s') % (i, im_get_candidate(i)) for i in range(num)))
                pass
            pass
        pass
    pass
